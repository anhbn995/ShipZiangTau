import json
from shapely import geometry
from rtree.index import Index
import math
import os
import random
import string

def distance(pointA, pointB):
    return math.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)
def random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


predict_file = r"G:\Shipdetection\ship-monitoring-ml2\haha\predict.geojson"
aoi_file = r"G:\Shipdetection\ship-monitoring-ml2\haha\aoi.geojson"
mask_file =r"G:\Shipdetection\ship-monitoring-ml2\haha\land.geojson"
output_path = r"G:\Shipdetection\ship-monitoring-ml2\haha\ok.geojson"


# open predict file and process ship
if predict_file is not None:
    with open(predict_file) as f:
        result = json.load(f)
    assert result['type'] == 'FeatureCollection', 'Land mask must be FeatureCollection, not {}'.format(result['type'])
    result_polygons = []
    for result_feature in result['features']:
        result_polygon = result_feature['geometry']['coordinates'][0]
        result_polygon = geometry.Polygon(result_polygon)
        mbr_points = list(zip(*result_polygon.minimum_rotated_rectangle.exterior.coords.xy))
        # print(mbr_points)
        result_polygons.append(mbr_points)
else:
    result_polygons = [] # result_polygons sẽ ở dạng shapely.geometry.polygon.Polygon object


shapely_polygons = []
for polygon in result_polygons:
    shapely_polygon = geometry.Polygon(polygon)
    shapely_polygons.append(shapely_polygon)

geo_polygons = []
for polygon in shapely_polygons:
    geo_polygon =  polygon.exterior.coords
    lengths = []
    for i in range(len(geo_polygon) - 1):
        lengths.append(distance(geo_polygon[i], geo_polygon[i + 1]))
    ship_length = max(lengths)
    geo_polygon = geometry.Polygon(geo_polygon)
    geo_polygons.append({'geometry': geo_polygon, 'length': ship_length})
# print(len(geo_polygons))

"""--------------"""
# open aoi file and mask file
# if aoi_file is not None:
#     with open(aoi_file) as f:
#         aoi = json.load(f)
#         # print(aoi)
#     assert aoi['type'] in ['FeatureCollection',
#                             'Feature'], 'AOI file must be Feature or FeatureCollection, not {}'.format(aoi['type'])

#     if aoi['type'] == 'FeatureCollection':
#         # only choose first feature, not support multiple polygon AOI
#         aoi_polygon = aoi['features'][0]['geometry']['coordinates'][0]
#     else:
#         aoi_polygon = aoi['geometry']['coordinates'][0]
#     aoi_polygon = geometry.Polygon(aoi_polygon)
# else:
#     aoi_polygon = None
# print(aoi_polygon)

if aoi_file is not None:
    with open(aoi_file) as f:
        aoi = json.load(f)
    assert aoi['type'] == 'FeatureCollection', 'Land mask must be FeatureCollection, not {}'.format(aoi['type'])
    aoi_polygons = []
    for aoi_feature in aoi['features']:
        aoi_polygon = aoi_feature['geometry']['coordinates'][0]
        aoi_polygon = geometry.Polygon(aoi_polygon)
        aoi_polygons.append(aoi_polygon)
else:
    aoi_polygons = []


if mask_file is not None:
    with open(mask_file) as f:
        masks = json.load(f)
    assert masks['type'] == 'FeatureCollection', 'Land mask must be FeatureCollection, not {}'.format(masks['type'])
    mask_polygons = []
    for mask_feature in masks['features']:
        mask_polygon = mask_feature['geometry']['coordinates'][0]
        mask_polygon = geometry.Polygon(mask_polygon)
        mask_polygons.append(mask_polygon)
else:
    mask_polygons = []

"""--------------------"""
# Check polygons inside of AOI and not intersect with land masks
not_land_polygons = []
for aoi_polygon in aoi_polygons:
    if aoi_polygon is not None:
        inside_aoi_polygons = []
        for polygon in geo_polygons:
            if aoi_polygon.intersects(polygon['geometry']):
                inside_aoi_polygons.append(polygon)
    else:
        inside_aoi_polygons = geo_polygons
           
    for polygon in inside_aoi_polygons:
        chosen = True
        for mask_polygon in mask_polygons:
            if mask_polygon.intersects(polygon['geometry']):
                chosen = False
        if chosen:
            not_land_polygons.append(polygon)

# check if polygon is valid
valid_polygons = []
for polygon in not_land_polygons:
    geom = polygon['geometry']
    minimum_surrounded_rectangle = geom.minimum_rotated_rectangle
    if minimum_surrounded_rectangle.geom_type == 'Polygon':
        valid_polygons.append(polygon)
final_polygons = valid_polygons
# print(final_polygons)


image_id = "20190123_031038_1034_3B_Visual"
detection_date = "20190123"
properties = {
    "ship_id": -1,
    "length": 0,
    "planet_image_id": image_id,
    "planet_image_source": "3-band (RGB) PlanetScope imagery that is framed as captured",
    "detect_date": detection_date,
    "accuracy": "high"
}

ship_boxes = []
features = []
for index, polygon in enumerate(final_polygons):
    ship_boxes.append(polygon['geometry'])
    geom = geometry.mapping(polygon['geometry'])
    props = properties.copy()
    ship_id = random_string(8)
    props.update(ship_id=ship_id)
    props.update(length=polygon['length'])
    feature = {'type': 'Feature', 'properties': props, 'geometry': geom}
    features.append(feature)
feature_collection = {'type': 'FeatureCollection', 'features': features}
with open(output_path, 'w') as dest:
    dest.write(json.dumps(feature_collection))