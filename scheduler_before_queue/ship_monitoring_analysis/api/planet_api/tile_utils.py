import json

import requests
from shapely.geometry import Polygon

from ship_monitoring_analysis.api.planet_api.globalmaptiles import GlobalMercator

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO

from skimage import io
import numpy as np
import random
import rasterio
from rasterio.windows import Window
from rasterio.transform import from_bounds
from rasterio.enums import ColorInterp
import concurrent.futures
from tqdm import tqdm

DOWNLOAD_URLs = [
    'https://tiles0.planet.com/v1/experimental/tiles/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles1.planet.com/v1/experimental/tiles/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles2.planet.com/v1/experimental/tiles/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles3.planet.com/v1/experimental/tiles/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles0.planet.com/data/v1/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles1.planet.com/data/v1/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles2.planet.com/data/v1/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
    'https://tiles3.planet.com/data/v1/{item_type}/{scene_id}/{z}/{x}/{y}.png?api_key={api_key}',
]

XYZ_BASEMAP_URLs = [
    'https://tiles0.planet.com/basemaps/v1/planet-tiles/{mosaic_name}/gmap/{z}/{x}/{y}.png?api_key={api_key}'
    'https://tiles1.planet.com/basemaps/v1/planet-tiles/{mosaic_name}/gmap/{z}/{x}/{y}.png?api_key={api_key}'
    'https://tiles2.planet.com/basemaps/v1/planet-tiles/{mosaic_name}/gmap/{z}/{x}/{y}.png?api_key={api_key}'
    'https://tiles3.planet.com/basemaps/v1/planet-tiles/{mosaic_name}/gmap/{z}/{x}/{y}.png?api_key={api_key}'
]

MOSAIC_MAP_URLs = [
    'https://tiles3.planet.com/experimental/mosaics/planet-tiles/global_monthly_{yy}_{m}_mosaic/gmap/{z}/{x}/{y}.png?token={token}',
    'https://tiles2.planet.com/experimental/mosaics/planet-tiles/global_monthly_{yy}_{m}_mosaic/gmap/{z}/{x}/{y}.png?token={token}',
    'https://tiles1.planet.com/experimental/mosaics/planet-tiles/global_monthly_{yy}_{m}_mosaic/gmap/{z}/{x}/{y}.png?token={token}'
]


def load_aoi_polygon(aoi_location, feature_id):
    with open(aoi_location) as f:
        return json.load(f)['features'][feature_id]['geometry']


def get_polygon_extend(points):
    geometry = Polygon(points)
    return geometry.bounds


def get_grid_offset(extent, zoom_level):
    lon, lat, max_lon, max_lat = extent
    mercator = GlobalMercator()
    tz = zoom_level
    min_x, min_y = mercator.LatLonToMeters(lat, lon)
    min_tx, min_ty = mercator.MetersToTile(min_x, min_y, tz)
    max_x, max_y = mercator.LatLonToMeters(max_lat, max_lon)
    max_tx, max_ty = mercator.MetersToTile(max_x, max_y, tz)
    return min_tx, min_ty, max_tx, max_ty


def get_grid_bound(xyz):
    tx, ty, tz = xyz
    mercator = GlobalMercator()
    lat_lon_bound = mercator.TileLatLonBounds(tx, ty, tz)
    return lat_lon_bound[1], lat_lon_bound[0], lat_lon_bound[3], lat_lon_bound[2]


def latlong_to_longlat(points):
    return map(lambda x: x[::-1], points)


def intersect(bound, polygon):
    # (xmin, ymin, xmax, ymax) -> topleft, topright, bottomright, bottomleft
    tl = (bound[0], bound[1])
    tr = (bound[2], bound[1])
    br = (bound[2], bound[3])
    bl = (bound[0], bound[3])
    poly_bound = Polygon([tl, tr, br, bl, tl])
    return poly_bound.intersects(polygon)


def tile_to_google_tile(xyz):
    tx, ty, tz = xyz
    mercator = GlobalMercator()
    gx, gy = mercator.GoogleTile(tx, ty, tz)
    return gx, gy, tz


def download_tile(xyz, year, month):
    gx, gy, tz = xyz
    index = random.randint(0, len(DOWNLOAD_URLs) - 1)
    print(index)
    url = DOWNLOAD_URLs[index].format(**{'yy': year, 'm': str(month).zfill(2), 'z': tz, 'x': gx, 'y': gy})
    session = requests.Session()
    session.headers.update({'referer': 'https://www.planet.com/explorer/'})
    result = session.get(url)
    return io.imread(StringIO(result.content))


def download(url):
    headers = {'referer': 'https://www.planet.com/explorer/'}
    return requests.get(url, headers=headers)


def concurrent_download_tiles(image_height, image_width, image_channel,
                              grid_index_list, urls, log_file=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        total_image = np.zeros((image_channel, image_height, image_width), dtype=np.uint8)
        future_to_url = {executor.submit(download, urls[i]): i for i in range(len(urls))}
        # images = [future.result() for future in concurrent.futures.as_completed(future_to_url)]
        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            k = future_to_url[future]
            # print(k)
            i, j = grid_index_list[k]
            try:
                result = io.imread(BytesIO(future.result().content))
            except Exception as e:
                print(future.result().content)
                continue
            if len(result.shape) >= 3:
                result = np.transpose(result, [2, 0, 1])
                total_image[:3, i * 256: (i + 1) * 256, j * 256: (j + 1) * 256] = result[:3]
                if result.shape[0] > 3:
                    total_image[3, i * 256: (i + 1) * 256, j * 256: (j + 1) * 256] = result[3]
                else:
                    total_image[3, i * 256: (i + 1) * 256, j * 256: (j + 1) * 256] = 255

            if log_file is not None:
                with open(log_file, 'a') as f:
                    f.write('{} {}\n'.format(i, j))
    return total_image


def concurrent_download_scene(image_height, image_width, image_channel, grid_index_list, google_grid_matrix,
                              dataset_location, item_type, api_key, scene_id, log_file=None):
    urls = []
    for k in range(grid_index_list.shape[0]):
        idx = random.randint(0, len(DOWNLOAD_URLs) - 1)
        gx, gy, tz = google_grid_matrix[grid_index_list[k][0], grid_index_list[k][1]]
        urls.append(DOWNLOAD_URLs[idx].format(
            **{'item_type': item_type, 'api_key': api_key, 'scene_id': scene_id, 'z': tz, 'x': gx, 'y': gy}))
    # start parallel use concurrent.futures
    total_image = concurrent_download_tiles(image_height, image_width, image_channel, grid_index_list, urls, log_file)
    with rasterio.open(dataset_location, 'r+') as dataset:
        dataset.write(total_image)


def concurrent_download_basemap(image_height, image_width, image_channel, grid_index_list, google_grid_matrix,
                                dataset_location, token, year, month, log_file=None):
    urls = []
    for k in range(grid_index_list.shape[0]):
        idx = random.randint(0, len(MOSAIC_MAP_URLs) - 1)
        gx, gy, tz = google_grid_matrix[grid_index_list[k][0], grid_index_list[k][1]]
        urls.append(MOSAIC_MAP_URLs[idx].format(
            **{'token': token, 'yy': year, 'm': month, 'z': tz, 'x': gx, 'y': gy}))
    # start parallel use concurrent.futures
    total_image = concurrent_download_tiles(image_height, image_width, image_channel, grid_index_list, urls, log_file)
    with rasterio.open(dataset_location, 'r+') as dataset:
        dataset.write(total_image)


def create_image(height, width, num_band, bound, output_file, driver='GTiff',
                 crs='+proj=latlong', nodata=0):
    transform = from_bounds(bound[0], bound[1], bound[2], bound[3],
                            width, height)

    with rasterio.open(output_file, 'w', driver=driver, bigtiff='YES', compress='LZW',
                       height=height, width=width,
                       count=num_band, dtype=rasterio.dtypes.uint8,
                       crs=crs, transform=transform, photometric='RBGA',
                       tiled=True, blockxsize=256, blockysize=256, interleave='band') as dst:
        dst.colorinterp = [ColorInterp.red, ColorInterp.green, ColorInterp.blue, ColorInterp.alpha]
    return output_file
