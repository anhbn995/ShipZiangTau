import os

import pandas as pd


def save_reporting_results(item_list, data_folder, delivery_folder, csv_report_path, pdf_report_path, shp_report_path,
                           reported_summary_file='reported_items.csv', column_name='item_id', use_index=False):
    reported_summary_file_path = os.path.join(data_folder, reported_summary_file)

    if os.path.exists(reported_summary_file_path):
        df = pd.read_csv(reported_summary_file_path)
        existed_items = df[column_name].tolist()
        new_items = [item_id for item_id in item_list if item_id not in existed_items]
    else:
        new_items = item_list
    new_df = pd.DataFrame(data=new_items, columns=[column_name])
    new_df['delivery_folder'] = delivery_folder
    new_df['csv_report_path'] = csv_report_path
    new_df['pdf_report_path'] = pdf_report_path
    new_df['shp_report_path'] = shp_report_path

    if os.path.exists(reported_summary_file_path):
        with open(reported_summary_file_path, 'a') as f:
            new_df.to_csv(f, header=False, index=use_index)
    else:
        new_df.to_csv(reported_summary_file_path, index=use_index)
