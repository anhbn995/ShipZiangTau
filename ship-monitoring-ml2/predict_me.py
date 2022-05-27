

import os
import sys

import json
import numpy as np
import rasterio
import cv2
from pyproj import Proj, transform
from shapely import geometry
from rtree.index import Index
import math
import random
import string

# Download and install the Python COCO tools from https://github.com/waleedka/coco
# That's a fork from the original https://github.com/pdollar/coco with a bug
# fix for Python 3.
# I submitted a pull request https://github.com/cocodataset/cocoapi/pull/50
# If the PR is merged then use the original repo.
# Note: Edit PythonAPI/Makefile and replace "python" with "python3".

# Root directory of the project
ROOT_DIR = os.path.abspath(r"G:\Shipdetection\scheduler_before_queue")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from ship_monitoring_analysis.ship_detection_algorithms.ship_detection_mask.mrcnn.config import Config
from ship_monitoring_analysis.ship_detection_algorithms.ship_detection_mask.mrcnn import model as modellib, utils

# Path to trained weights file
# COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
# DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")
DEFAULT_DATASET_YEAR = "2014"


############################################################
#  Configurations
############################################################


class AirbusShipConfig(Config):
    """Configuration for training on the ship dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "ship"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + ship

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    DETECTION_NMS_THRESHOLD = 0.7


def pixel_to_geographic_location(pixel_location, origin, resolution_x, resolution_y):
    x = origin[0] + pixel_location[0] * resolution_x
    y = origin[1] - pixel_location[1] * resolution_y
    return x, y


def distance(pointA, pointB):
    return math.sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)


def random_string(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


def predictor(weights_path):
    class InferenceConfig(AirbusShipConfig):
        # Set batch size to 1 since we'll be running inference on
        # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()

    config.display()

    # Create model
    model = modellib.MaskRCNN(mode="inference", config=config,
                              model_dir=os.path.dirname(weights_path))

    # Load weights
    model.load_weights(weights_path, by_name=True)

    return model


def main_predict(model, image_id, image_path, output_path,
                 aoi_file, mask_file, detection_date, chunk_size=512, padding_size=200):
    # Run model detection and save to file
    print("Running on {}".format(image_path))
    # Read image
    with rasterio.open(image_path) as src:
        image = src.read((1, 2, 3))
        image_width = src.width
        image_height = src.height
        origin = (src.bounds.left, src.bounds.top)
        res_x, res_y = src.res
        crs = src.crs
        profile = src.profile

    image = np.transpose(image, (1, 2, 0))
    # Detect cells
    polygons = []
    scores = []
    if image_width <= chunk_size and image_height <= chunk_size:
        results = model.detect([image], verbose=0)
        print('number of results:', len(results))
        result = results[0]
        if result['masks'].shape[-1] > 0:
            for i in range(result['masks'].shape[-1]):
                scores.append(result['scores'][i])
                splash = result['masks'][:, :, i]
                splash = splash.astype(np.uint8)

                major = cv2.__version__.split('.')[0]
                if major == '3':
                    _, contours, hierarchy = cv2.findContours(splash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                else:
                    contours, hierarchy = cv2.findContours(splash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                cnt = contours[0]
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                print("duc anh aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",box)
                print("duc anh bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",rect)
                polygons.append(box)
    else:
        padded_image = np.pad(image, pad_width=((padding_size, padding_size), (padding_size, padding_size), (0, 0)),
                              mode='reflect')
        cells = []
        num_cols = image_height // chunk_size
        num_rows = image_width // chunk_size

        for i in range(num_cols):
            for j in range(num_rows):
                start_i = i * chunk_size
                if i == (num_cols - 1):
                    end_i = image_height
                else:
                    end_i = (i + 1) * chunk_size

                start_j = j * chunk_size
                if j == (num_rows - 1):
                    end_j = image_width
                else:
                    end_j = (j + 1) * chunk_size
                cell = padded_image[start_i:end_i + padding_size * 2, start_j:end_j + padding_size * 2, :]
                cells.append({'image': cell, 'i': i, 'j': j})

        for cell in cells:
            cell_image = cell['image']
            i = cell['i']
            j = cell['j']
            offset_i = i * chunk_size - padding_size
            offset_j = j * chunk_size - padding_size
            results = model.detect([cell_image], verbose=0)
            result = results[0]
            if result['masks'].shape[-1] > 0:
                # total_mask = []
                for i in range(result['masks'].shape[-1]):
                    scores.append(result['scores'][i])
                    splash = result['masks'][:, :, i]
                    splash = splash.astype(np.uint8)
                    major = cv2.__version__.split('.')[0]
                    if major == '3':
                        _, contours, hierarchy = cv2.findContours(splash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    else:
                        contours, hierarchy = cv2.findContours(splash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        cnt = contours[0]
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.asarray(box) + [offset_j, offset_i]
                        polygons.append(box.tolist())

    p1 = Proj(init=crs.to_dict()['init'])
    p2 = Proj(init='epsg:4326')

    shapely_polygons = []
    for polygon in polygons:
        shapely_polygon = geometry.Polygon(polygon)
        shapely_polygons.append(shapely_polygon)

    # generate Rtree index for faster intersection checking
    idx = Index()
    for pos, polygon in enumerate(shapely_polygons):
        idx.insert(pos, polygon.bounds)

    not_intersect_polygons = []
    chosen_intersect_indexes = []
    # filter intersect polygons, choose the highest score.
    for index, polygon in enumerate(shapely_polygons):
        intersection_indexes = list(idx.intersection(polygon.bounds))
        intersection_index_set = set(intersection_indexes)
        intersection_index_set.discard(index)
        if intersection_index_set:
            max_score_index = None
            max_score = 0
            for i in intersection_indexes:
                if scores[i] > max_score:
                    max_score_index = i
                    max_score = scores[i]
            chosen_intersect_indexes.append(max_score_index)
        else:
            not_intersect_polygons.append(polygon)

    # print(len(not_intersect_polygons))
    chosen_intersect_indexes = set(chosen_intersect_indexes)
    chosen_intersect_polygons = [shapely_polygons[i] for i in chosen_intersect_indexes]
    # print(len(chosen_intersect_polygons))

    filtered_polygons = not_intersect_polygons + chosen_intersect_polygons

    geo_polygons = []
    for polygon in filtered_polygons:
        geo_polygon = [pixel_to_geographic_location(point, origin, res_x, res_y) for point in polygon.exterior.coords]
        lengths = []
        for i in range(len(geo_polygon) - 1):
            lengths.append(distance(geo_polygon[i], geo_polygon[i + 1]))
        ship_length = max(lengths)
        geo_polygon = [transform(p1, p2, x, y) for x, y in geo_polygon]
        geo_polygon = geometry.Polygon(geo_polygon)
        geo_polygons.append({'geometry': geo_polygon, 'length': ship_length})
    print(len(geo_polygons))

    # open aoi file and mask file
    if aoi_file is not None:
        with open(aoi_file) as f:
            aoi = json.load(f)
            print(aoi)
        assert aoi['type'] in ['FeatureCollection',
                               'Feature'], 'AOI file must be Feature or FeatureCollection, not {}'.format(aoi['type'])

        if aoi['type'] == 'FeatureCollection':
            # only choose first feature, not support multiple polygon AOI
            aoi_polygon = aoi['features'][0]['geometry']['coordinates'][0]
        else:
            aoi_polygon = aoi['geometry']['coordinates'][0]
        aoi_polygon = geometry.Polygon(aoi_polygon)
    else:
        aoi_polygon = None

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
    # Check polygons inside of AOI and not intersect with land masks
    if aoi_polygon is not None:
        inside_aoi_polygons = []
        for polygon in geo_polygons:
            if aoi_polygon.intersects(polygon['geometry']):
                inside_aoi_polygons.append(polygon)
    else:
        inside_aoi_polygons = geo_polygons

    not_land_polygons = []
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
    # print(len(final_polygons))
    print(final_polygons)

    schema = {'geometry': 'Polygon', 'properties': {}}
    image_name = os.path.basename(image_path)

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
    return ship_boxes


############################################################
#  Training
############################################################

if __name__ == '__main__':
    # import argparse

    # # Parse command line arguments
    # parser = argparse.ArgumentParser(
    #     description='Train Mask R-CNN to detect ship.')
    # parser.add_argument('--weights', required=True,
    #                     metavar="/path/to/weights.h5",
    #                     help="Path to weights .h5 file or 'coco'")
    # parser.add_argument('--image', required=True,
    #                     metavar="path or URL to image",
    #                     help='Image to apply detection on')
    # parser.add_argument('--output', required=True,
    #                     help='path of output result')
    # parser.add_argument('--aoi', required=True,
    #                     help='path of aoi file, day la vung nguoi ta quan tam')
    # parser.add_argument('--mask', required=True,
    #                     help='path of land mask file, day la vung dat')
    # parser.add_argument('--date', required=True,
    #                     help='detection date')
    # args = parser.parse_args()

    # assert args.image, \
    #     "Provide --image to apply color splash"

    # print("Weights: ", args.weights)
    
    # # Train or evaluate
    # model = predictor(args.weights)
    # main_predict(model, args.image, args.output, args.aoi, args.mask, args.date)
# """ cai nay ok """
    # model_path = r"E:\Shipdetection\Run\model\mask_rcnn_ship_0358.h5"
    # image_id = "20190123_031038_1034_3B_Visual"
    # image_path = r"E:\Shipdetection\Run\base\AOI_Bengkalis\20190123_031038_1034_3B_Visual.tif"
    # output_path = r"E:\Shipdetection\Code_dung_lai\20190123_031038_1034_3B_Visual.geojson"
    # aoi_path = r"E:\Shipdetection\Run\oai\AOI_Bengkalis.geojson"
    # mask_land_path = r"E:\Shipdetection\Run\mask_folder\AOI_Bengkalis_LandMask.geojson"
    # date_time = "20190123"


    """ cai nay ok """
    model_path = r"G:\Shipdetection\ship-monitoring-ml2\model\mask_rcnn_ship_0358.h5"
    image_id = "20190123_031038_1034_3B_Visual"
    image_path = r"G:\Shipdetection\ship-monitoring-ml2\download.tiff"
    output_path = r"G:\Shipdetection\ship-monitoring-ml2\download.geojson"
    aoi_path = r"G:\Shipdetection\ship-monitoring-ml2\aoi\AOI_Semiun.geojson"
    mask_land_path = r"G:\Shipdetection\ship-monitoring-ml2\mask_folder\AOI_Semiun_LandMask.geojson"
    date_time = "20190123"

    model = predictor(model_path)
    main_predict(model, image_id, image_path, output_path, aoi_path, mask_land_path, date_time)


