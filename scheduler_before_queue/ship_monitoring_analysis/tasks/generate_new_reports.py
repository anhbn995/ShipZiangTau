import json
import os

import pandas as pd

from ship_monitoring_analysis.reporting import (generate_ship_csv, generate_ship_pdf, generate_ship_shapefiles)


def generate_reports(aoi_file, aoi_name, run_date, api_key, email, password, data_folder, delivery_folder,
                     output_filename, downloaded_file='downloaded_items.csv', predicted_file='predicted_items.csv',
                     execute_path=None):
    # get all item information into 1 dict - predicted_item_info
    predicted_file_path = os.path.join(data_folder, predicted_file)
    downloaded_file_path = os.path.join(data_folder, downloaded_file)
    predicted_df = pd.read_csv(predicted_file_path)
    downloaded_df = pd.read_csv(downloaded_file_path)
    predicted_item_info = {}
    for index, row in predicted_df.iterrows():
        item_id = row['item_id']
        result_file_path = row['result_path']
        predicted_item_info[item_id] = {'result_path': result_file_path}
    for index, row in downloaded_df.iterrows():
        item_id = row['item_id']
        item_downloaded_file = row['downloaded_file']
        item_info = row['item_info']
        item_info = json.loads(item_info)
        if item_id in predicted_item_info:
            predicted_item_info[item_id].update(downloaded_file=item_downloaded_file, item_info=item_info)
    # set output_file's name
    csv_output_file = os.path.join(delivery_folder, output_filename + '.csv')
    pdf_output_file = os.path.join(delivery_folder, output_filename + '.pdf')
    zip_output_file = os.path.join(delivery_folder, output_filename + '.zip')
    # save information to csv format (a part of delivery)
    ship_total_df = generate_ship_csv.generate_ship_csv(predicted_item_info, csv_output_file)
    # save information to pdf format (a part of delivery)
    generate_ship_pdf.generate_pdf_report(predicted_item_info, ship_total_df, aoi_file, aoi_name, run_date,
                                          delivery_folder, email, password, pdf_output_file)
    # save detection results to shapefile format
    generate_ship_shapefiles.generate_ship_shapefiles(predicted_item_info, delivery_folder, zip_output_file,
                                                      execute_path)
    return csv_output_file, pdf_output_file, zip_output_file
