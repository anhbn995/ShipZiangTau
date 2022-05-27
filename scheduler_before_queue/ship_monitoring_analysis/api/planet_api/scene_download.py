import os
import time

import numpy as np
from planet import api
from pyproj import Proj
from shapely.geometry import Polygon

from ship_monitoring_analysis.api.planet_api import tile_utils


def mosaic_download(output_file, bound, token, month, year, zoom_level=15):
    # get grids to download
    offset = tile_utils.get_grid_offset(bound, zoom_level=zoom_level)
    # print(offset)
    grid_matrix = np.zeros((offset[3] - offset[1] + 1, offset[2] - offset[0] + 1, 3), dtype=np.uint32)
    height, width, _ = grid_matrix.shape
    print(grid_matrix.shape)

    for i in range(height):
        for j in range(width):
            grid_matrix[i, j] = (offset[0] + j, offset[3] - i, zoom_level)

    bound_matrix = np.reshape(
        np.apply_along_axis(tile_utils.get_grid_bound, 1, grid_matrix.reshape(width * height, 3)), (height, width, 4))

    # intersect_grid_matrix = np.reshape(
    #     np.apply_along_axis(tile_utils.intersect, 1, bound_matrix.reshape(width * height, 4), polygon), (height, width))
    intersect_grid_matrix = np.full((height, width), True, dtype=np.bool)
    # convert to google grid before create link download
    google_grid_matrix = np.reshape(
        np.apply_along_axis(tile_utils.tile_to_google_tile, 1, grid_matrix.reshape(width * height, 3)),
        (height, width, 3)
    ).astype(np.uint32)

    grid_index_list = np.array(np.where(intersect_grid_matrix)).transpose()
    print(grid_index_list.shape)

    # create dataset
    west = bound_matrix[0, 0][0]
    north = bound_matrix[0, 0][3]
    east = bound_matrix[-1, -1][2]
    south = bound_matrix[-1, -1][1]
    bound = (west, south, east, north)
    print(bound)
    projector = Proj(init='epsg:3857')
    west, north = projector(west, north)
    east, south = projector(east, south)
    new_bound = (west, south, east, north)
    print(new_bound)

    crs = {'init': 'epsg:3857'}
    dataset_location = tile_utils.create_image(256 * height, 256 * width, 4, new_bound, output_file, crs=crs)

    start_time = time.time()
    tile_utils.concurrent_download_basemap(256 * height, 256 * width, 4, grid_index_list, google_grid_matrix,
                                           dataset_location, token, year, month)
    print('time spend on download:{}'.format(time.time() - start_time))


def download_single_scene_tile(item_type, scene_id, api_key, output_file, zoom_level=15):
    # get scene bounding box
    client = api.ClientV1(api_key=api_key)
    result = client.get_item(item_type, scene_id)
    response = result.get()
    permissions = response['_permissions']
    if not permissions:
        raise Exception('API Key does not have permission to download')
    polygon = response['geometry']['coordinates'][0]
    polygon = Polygon(polygon)
    # print(polygon.wkt)
    # get bound
    extent = polygon.bounds

    # get grids to download
    offset = tile_utils.get_grid_offset(extent, zoom_level=zoom_level)
    # print(offset)
    grid_matrix = np.zeros((offset[3] - offset[1] + 1, offset[2] - offset[0] + 1, 3), dtype=np.uint32)
    height, width, _ = grid_matrix.shape
    print(grid_matrix.shape)

    for i in range(height):
        for j in range(width):
            grid_matrix[i, j] = (offset[0] + j, offset[3] - i, zoom_level)

    bound_matrix = np.reshape(
        np.apply_along_axis(tile_utils.get_grid_bound, 1, grid_matrix.reshape(width * height, 3)), (height, width, 4))

    intersect_grid_matrix = np.reshape(
        np.apply_along_axis(tile_utils.intersect, 1, bound_matrix.reshape(width * height, 4), polygon), (height, width))

    # convert to google grid before create link download
    google_grid_matrix = np.reshape(
        np.apply_along_axis(tile_utils.tile_to_google_tile, 1, grid_matrix.reshape(width * height, 3)),
        (height, width, 3)
    ).astype(np.uint32)

    grid_index_list = np.array(np.where(intersect_grid_matrix)).transpose()
    print(grid_index_list.shape)

    # create dataset
    west = bound_matrix[0, 0][0]
    north = bound_matrix[0, 0][3]
    east = bound_matrix[-1, -1][2]
    south = bound_matrix[-1, -1][1]
    bound = (west, south, east, north)
    print(bound)
    projector = Proj(init='epsg:3857')
    west, north = projector(west, north)
    east, south = projector(east, south)
    new_bound = (west, south, east, north)
    print(new_bound)

    crs = {'init': 'epsg:3857'}
    dataset_location = tile_utils.create_image(256 * height, 256 * width, 4, new_bound, output_file, crs=crs)

    start_time = time.time()
    tile_utils.concurrent_download_scene(256 * height, 256 * width, 4, grid_index_list, google_grid_matrix, dataset_location, item_type, api_key, scene_id)
    print('time spend on download:{}'.format(time.time() - start_time))


def download_scene_tiles(api_key, scene_ids, output_format, zoom_level=15, item_type='PSScene3Band'):
    for scene_id in scene_ids:
        try:
            output_file = output_format.format(item_id=scene_id)
            download_single_scene_tile(item_type, scene_id, api_key, output_file, zoom_level)
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    # get config
    __item_type = 'PSScene3Band'
    __scene_id = '20190316_022435_1040'
    __api_key = '1221cfc2e35a4b8b838245a88aa96a50'
    __output_file = '/media/giangblackk/Data0/skymapdev/indonesia_ship/brunei_customer/deploy/tile_data/20190316/{}_3B_Tile_Write_Once.tif'.format(
        __scene_id)
    __zoomLevel = 15
    download_single_scene_tile(__item_type, __scene_id, __api_key, __output_file, __zoomLevel)
