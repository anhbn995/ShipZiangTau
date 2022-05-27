import json
import os

import rasterio
from osgeo import gdal
from pyproj import Proj, transform
from shapely import geometry


def warp_image(input_image, output_image, aoi_file, tmp_bound_file):
    tmp_bound_filename = os.path.basename(tmp_bound_file)
    layer_name = os.path.splitext(tmp_bound_filename)[0]

    with open(aoi_file, 'r') as f:
        aoi = json.load(f)
        if aoi['type'] == 'Feature':
            aoi_polygon = aoi['geometry']['coordinates'][0]
        elif aoi['type'] == 'FeatureCollection':
            aoi_polygon = aoi['features'][0]['geometry']['coordinates'][0]
        else:
            raise Exception('AOI type doen\'t match Feature or FeatureCollection')

    with rasterio.open(input_image, 'r') as src:
        src_crs = src.crs
        left, bottom, right, top = tuple(src.bounds)

    p0 = Proj(init='epsg:4326')
    p1 = Proj(init=src_crs.to_dict()['init'])
    aoi_polygon = [p1(point[0], point[1]) for point in aoi_polygon]
    aoi_polygon = geometry.Polygon(aoi_polygon)

    image_polygon = [(left, top), (right, top), (right, bottom), (left, bottom), (left, top)]
    image_polygon = geometry.Polygon(image_polygon)

    if not aoi_polygon.intersects(image_polygon):
        print('image bound does not intersect with aoi')
        return None
    intersection_polygon = aoi_polygon.intersection(image_polygon)
    intersection_polygon_coords = list(intersection_polygon.exterior.coords)
    intersection_polygon_coords = [transform(p1, p0, point[0], point[1]) for point in intersection_polygon_coords]
    intersection_feature = {'type': 'Feature', 'properties': {}}
    intersection_feature['geometry'] = {'type': 'Polygon', 'coordinates': [intersection_polygon_coords]}
    with open(tmp_bound_file, 'w') as f:
        json.dump(intersection_feature, f)

    warp_options = gdal.WarpOptions(format='GTiff',
                                    cutlineDSName=tmp_bound_file, cutlineLayer=layer_name, cropToCutline=True)
    gdal.Warp(output_image, input_image, options=warp_options)
    return output_image
