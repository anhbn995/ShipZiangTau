import os
import pandas as pd


def get_reported_items(data_folder, reported_summary_file='reported_items.csv', column_name='item_id'):
    reported_summary_filepath = os.path.join(data_folder, reported_summary_file)
    if os.path.exists(reported_summary_filepath):
        df = pd.read_csv(reported_summary_filepath)
        reported_items = df[column_name].tolist()
        return reported_items
    else:
        return list()
