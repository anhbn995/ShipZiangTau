import cv2
import numpy as np
import rasterio
from pyproj import Proj


def geographic_to_pixel_location(point, origin, res_x, res_y):
    return (point[0] - origin[0]) / res_x, -1. * (point[1] - origin[1]) / res_y


def draw_polygon_on_image(image, polygons, origin, res_x, res_y, crs, colors):
    copy_image = image.copy()
    p1 = Proj(init=crs.to_dict()['init'])
    pixel_polygons = []
    for polygon in polygons:
        projected_polygon = [p1(point[0], point[1]) for point in polygon]
        pixel_polygon = [geographic_to_pixel_location(point, origin, res_x, res_y) for point in projected_polygon]
        pixel_polygons.append(pixel_polygon)

    for polygon in pixel_polygons:
        pts = np.array(polygon).astype(np.int32)
        pts = pts.reshape((-1, 1, 2))

        cv2.polylines(copy_image, [pts], True, colors, thickness=2)

    return copy_image


def draw_polygon_on_dataset(image_file, polygons):
    with rasterio.open(image_file, 'r') as src:
        image = src.read((1, 2, 3))
        origin = (src.bounds.left, src.bounds.top)
        res_x, res_y = src.res
        crs = src.crs

    copy_image = np.transpose(image, (1, 2, 0)).copy()
    p1 = Proj(init=crs.to_dict()['init'])
    pixel_polygons = []
    for polygon in polygons:
        projected_polygon = [p1(point[0], point[1]) for point in polygon]
        pixel_polygon = [geographic_to_pixel_location(point, origin, res_x, res_y) for point in projected_polygon]
        pixel_polygons.append(pixel_polygon)

    for polygon in pixel_polygons:
        pts = np.array(polygon).astype(np.int32)
        pts = pts.reshape((-1, 1, 2))

        cv2.polylines(copy_image, [pts], True, (0, 255, 255))

    return copy_image


def draw_point_on_dataset(image_file, points, radius=10, color=(0, 0, 255)):
    with rasterio.open(image_file, 'r') as src:
        image = src.read((1, 2, 3))
        origin = (src.bounds.left, src.bounds.top)
        res_x, res_y = src.res
        crs = src.crs

    copy_image = np.transpose(image, (1, 2, 0)).copy()
    p1 = Proj(init=crs.to_dict()['init'])
    pixel_points = []
    for point in points:
        projected_point = p1(point[0], point[1])
        pixel_point = geographic_to_pixel_location(projected_point, origin, res_x, res_y)
        pixel_points.append((
            round(pixel_point[0]), round(pixel_point[1])
        ))

    for point in pixel_points:
        cv2.circle(copy_image, point, radius, color, -1)
    return copy_image


def draw_text(image, content, position, font_scale, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    copy_image = image.copy()
    return cv2.putText(copy_image, content, position, font, font_scale, color, 2, cv2.LINE_AA)
