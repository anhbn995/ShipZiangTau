import json
import os

import pandas as pd
from pyproj import Proj
from shapely import geometry


# only apply to simple polygon (without holes)
def get_segment_lengths(polygon):
    points = list(polygon.exterior.coords)
    lines = [geometry.LineString((p1, p2)) for p1, p2 in zip(points[1:], points[:-1])]
    lengths = [line.length for line in lines]
    return lengths


# assume that rotated rectangle has length > width
def get_length_width_rotate_rect(rotated_rectangle):
    segment_lengths = get_segment_lengths(rotated_rectangle)
    length = max(segment_lengths)
    width = min(segment_lengths)
    return length, width


def generate_ship_csv(predicted_item_info, output_csv_file):
    p1 = Proj(init='epsg:3857')
    ship_dfs = []
    for item_id, item_info in predicted_item_info.items():
        result_file_path = item_info['result_path']
        strip_id = item_info['item_info']['properties']['strip_id']
        with open(result_file_path, 'r') as f:
            ship_collection = json.load(f)
        ship_rows = []
        for feature in ship_collection['features']:
            ship_id = feature['properties']['ship_id']
            ship_row = {'ship_id': ship_id, 'item_id': item_id, 'group_id': strip_id}
            # get center
            ship_box = feature['geometry']['coordinates'][0]
            polygon = geometry.Polygon(ship_box)
            centroid = polygon.centroid
            ship_row['longitude'] = centroid.x
            ship_row['latitude'] = centroid.y
            # get width and height
            geo_ship_box = [p1(point[0], point[1]) for point in ship_box]
            geo_polygon = geometry.Polygon(geo_ship_box)
            minimum_surrounded_rectangle = geo_polygon.minimum_rotated_rectangle
            length, width = get_length_width_rotate_rect(minimum_surrounded_rectangle)
            ship_row['length'] = length
            ship_rows.append(ship_row)
        ship_df = pd.DataFrame(ship_rows,
                               columns=['ship_id', 'item_id', 'group_id', 'longitude', 'latitude', 'length'])
        ship_dfs.append(ship_df)
    if ship_dfs:
        ship_total_df = pd.concat(ship_dfs, ignore_index=True)
    else:
        ship_total_df = pd.DataFrame(columns=['ship_id', 'item_id', 'group_id', 'longitude', 'latitude', 'length'])
    ship_total_df.to_csv(output_csv_file, index=True, header=True, index_label='index')
    return ship_total_df
