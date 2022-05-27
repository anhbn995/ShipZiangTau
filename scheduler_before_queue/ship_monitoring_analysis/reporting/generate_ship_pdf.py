import colorsys
import json
import os
import random

import numpy as np
import pandas as pd
import rasterio
from dateutil import relativedelta, parser as date_parser
from pyproj import Proj
from shapely import geometry
from shapely.ops import cascaded_union

from ship_monitoring_analysis.api.planet_api import scene_download, get_token
from ship_monitoring_analysis.reporting import template
from ship_monitoring_analysis.reporting.image import (draw_polygon_on_image, draw_text,
                                                      draw_point_on_dataset, geographic_to_pixel_location)
from ship_monitoring_analysis.utils import warp, misc


def download_basemap(item_dict, aoi_file, aoi_name, start_date, delivery_folder, email, password):
    # download basemap of AOI for summary
    basemap_datetime = start_date + relativedelta.relativedelta(months=-2)
    basemap_year = basemap_datetime.year
    basemap_month = basemap_datetime.month
    basemap_month = str(basemap_month).zfill(2)

    with open(aoi_file, 'r') as f:
        aoi = json.load(f)
    if aoi['type'] == 'Feature':
        aoi_polygon = aoi['geometry']['coordinates'][0]
    else:
        assert aoi['type'] == 'FeatureCollection'
        aoi_polygon = aoi['features'][0]['geometry']['coordinates'][0]
    aoi_polygon = geometry.Polygon(aoi_polygon)
    polygons = [aoi_polygon]

    for item_id, item_info in item_dict.items():
        coords = item_info['item_info']['geometry']['coordinates'][0]
        polygons.append(geometry.Polygon(coords))

    union_polygon = cascaded_union(polygons)
    # print(union_polygon)
    bounds = union_polygon.bounds

    basemap_file = os.path.join(delivery_folder, 'basemap_{}_{}_{}.tif'.format(aoi_name, basemap_month, basemap_year))
    token = get_token.get_planet_auth_token(email, password)
    scene_download.mosaic_download(basemap_file, bounds, token, month=basemap_month, year=basemap_year, zoom_level=11)
    return basemap_file


def warp_images(item_dict, aoi_file):
    updated_item_dict = item_dict.copy()
    for image_id, image_info in item_dict.items():
        input_file = image_info['downloaded_file']
        if input_file:
            output_file = input_file.replace('.tif', '_Warp.tif')
            tmp_file = os.path.splitext(input_file)[0] + '.clipped.geojson'
            warp.warp_image(input_file, output_file, aoi_file, tmp_file)
            updated_item_dict[image_id].update(warp_image_path=output_file)
    return updated_item_dict


def draw_on_basemap(item_dict, basemap_file, aoi_file):
    aoi_polygon = misc.single_feature_geojson_to_shapely(aoi_file)
    with rasterio.open(basemap_file) as src:
        basemap_image = src.read((1, 2, 3))
        basemap_image = np.transpose(basemap_image, (1, 2, 0))
        origin = (src.bounds.left, src.bounds.top)
        res_x, res_y = src.res
        crs = src.crs

    p1 = Proj(init=crs.to_dict()['init'])
    drawn_basemap = draw_polygon_on_image(basemap_image, [list(aoi_polygon.exterior.coords)],
                                          origin, res_x, res_y, crs, (0, 255, 255))

    strips = {}
    for item_id, item_info in item_dict.items():
        strip_id = item_info['item_info']['properties']['strip_id']
        if strip_id in strips:
            strips[strip_id].append(item_id)
        else:
            strips[strip_id] = [item_id]

    for strip_id, item_ids in strips.items():
        strip_polygons = []
        random_color = colorsys.hsv_to_rgb(random.random(), 1., random.random())
        random_color = list(round(x * 255) for x in random_color)
        top_points = []

        for item_id in item_ids:
            coords = item_dict[item_id]['item_info']['geometry']['coordinates'][0]
            strip_polygons.append(coords)
        drawn_basemap = draw_polygon_on_image(drawn_basemap, strip_polygons, origin, res_x, res_y, crs, random_color)

        for item_id in item_ids:
            coords = item_dict[item_id]['item_info']['geometry']['coordinates'][0]
            label_location = sorted(coords, key=lambda p: p[0])[0]  # left most point
            top_point = sorted(coords, key=lambda p: p[1])[-1]
            top_points.append(top_point)
            label_location = p1(label_location[0], label_location[1])
            label_location = geographic_to_pixel_location(label_location, origin, res_x, res_y)
            label_location = (round(label_location[0]), round(label_location[1]))
            drawn_basemap = draw_text(drawn_basemap, item_id, label_location, 0.5, (0, 255, 0))

        top_group_point = sorted(top_points, key=lambda p: p[1])[-1]
        top_group_point = p1(top_group_point[0], top_group_point[1])
        top_group_point = geographic_to_pixel_location(top_group_point, origin, res_x, res_y)
        top_group_point = (round(top_group_point[0]), round(top_group_point[1]))
        drawn_basemap = draw_text(drawn_basemap, strip_id, top_group_point, 1, (255, 0, 0))
    return drawn_basemap


def draw_on_warp_images(item_dict, ship_total_df):
    updated_item_dict = item_dict.copy()
    for item_id in item_dict.keys():
        item_ship_df = ship_total_df[ship_total_df.item_id == item_id]
        ship_points = []
        for index, row in item_ship_df.iterrows():
            ship_points.append((row['longitude'], row['latitude']))
        ship_drawn_image = draw_point_on_dataset(item_dict[item_id]['warp_image_path'], ship_points)
        updated_item_dict[item_id]['ship_image'] = ship_drawn_image
    return updated_item_dict


def create_pdf(item_dict, ship_total_df, drawn_basemap, start_date, aoi_name, output_report_file):
    summary_table = [['Id', 'Group Id', 'Satellite Id', 'Start Acquired Time', 'Number of Scene']]
    count = 0
    strips = {}
    for item_id, item_info in item_dict.items():
        strip_id = item_info['item_info']['properties']['strip_id']
        if strip_id in strips:
            strips[strip_id].append(item_id)
        else:
            strips[strip_id] = [item_id]

    for strip_id, item_ids in strips.items():
        number_of_scenes = len(item_ids)
        acquired_times = [date_parser.parse(item_dict[item_id]['item_info']['properties']['acquired']) for item_id in
                          item_ids]
        satellite_id = item_dict[item_ids[0]]['item_info']['properties']['satellite_id']
        start_acquired_time = min(acquired_times)
        summary_table.append([
            count,
            strip_id,
            satellite_id,
            start_acquired_time.strftime('%d-%m-%Y %H:%M:%S') + ' UTC',
            number_of_scenes
        ])
        count += 1

    strip_dfs = []
    for strip_id, item_ids in strips.items():
        rows = []
        for item_id in item_ids:
            item_ship_df = ship_total_df[ship_total_df.item_id == item_id]
            number_of_ship = len(item_ship_df)
            acquired_time = date_parser.parse(item_dict[item_id]['item_info']['properties']['acquired']).strftime(
                '%d-%m-%Y %H:%M:%S') + ' UTC'
            rows.append([strip_id, item_id, acquired_time, number_of_ship])
        strip_df = pd.DataFrame(rows, columns=['strip_id', 'item_id', 'acquired', 'num_ships'])
        strip_dfs.append(strip_df)
    if strip_dfs:
        total_strip_df = pd.concat(strip_dfs, ignore_index=True)
    else:
        total_strip_df = pd.DataFrame(columns=['strip_id', 'item_id', 'acquired', 'num_ships'])
    ######################################### generate report only ###########################
    # Company Info
    report_parts = []

    report_parts.append(template.spacer())
    report_parts.append(template.spacer())

    # Report Summary part
    report_parts.extend(template.title("Ship Detection Report for {}".format(start_date)))

    report_parts.append(template.subtitle("1. Summary of Ship Detection"))

    report_parts.extend(template.summary(aoi_name, start_date))
    report_parts.extend(template.image(drawn_basemap))
    report_parts.append(template.table(summary_table))

    report_parts.append(template.spacer())
    report_parts.append(template.spacer())

    report_parts.append(template.subtitle("2. Detailed Report"))

    for strip_id, item_ids in strips.items():
        # add Group title and group table
        report_parts.append(template.subtitle('Group {}'.format(strip_id)))
        strip_table = [['Id', 'Scene Id', 'Acquired Time', 'Number of Ship']]
        strip_df = total_strip_df[total_strip_df.strip_id == strip_id]
        for index, row in strip_df.iterrows():
            strip_table.append([index, row['item_id'], row['acquired'], row['num_ships']])
        if len(strip_table) > 1:
            report_parts.append(template.table(strip_table))

        for item_id in item_ids:
            item = item_dict[item_id]
            report_parts.append(template.subsubtitle("Image " + str(item_id)))
            # create table data
            item_table = [['Ship Id', 'Longitude', 'Latitude', 'Length (m)']]
            # filter data_frame to fill table
            item_ship_df = ship_total_df[ship_total_df.item_id == item_id]
            for index, row in item_ship_df.iterrows():
                item_table.append([row['ship_id'], row['longitude'], row['latitude'], row['length']])
            # item image (open image, draw on it, resize it and save to temporary file)
            report_parts.extend(template.image(item_dict[item_id]['ship_image']))

            # item table
            if len(item_table) > 1:
                report_parts.append(template.table(item_table))
            report_parts.append(template.spacer())
        report_parts.append(template.spacer())
        report_parts.append(template.line())

    # Build report pdf
    template.build_report(report_parts, output_report_file)


def generate_pdf_report(predicted_item_info, ship_total_df, aoi_file, aoi_name,
                        start_date, delivery_folder, email, password, output_pdf_file):
    # download basemap file
    basemap_file = download_basemap(predicted_item_info, aoi_file, aoi_name,
                                    start_date, delivery_folder, email, password)
    # warp image
    updated_item_info = warp_images(predicted_item_info, aoi_file)
    drawn_basemap = draw_on_basemap(updated_item_info, basemap_file, aoi_file)
    updated_item_info = draw_on_warp_images(updated_item_info, ship_total_df)
    create_pdf(updated_item_info, ship_total_df, drawn_basemap, start_date, aoi_name, output_pdf_file)
