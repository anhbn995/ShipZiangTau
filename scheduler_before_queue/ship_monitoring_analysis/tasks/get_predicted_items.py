import os
import pandas as pd


def get_predicted_items(data_folder, predicted_summary_file='predicted_items.csv', column_name='item_id'):
    predicted_summary_filepath = os.path.join(data_folder, predicted_summary_file)
    if os.path.exists(predicted_summary_filepath):
        df = pd.read_csv(predicted_summary_filepath)
        reported_items = df[column_name].tolist()
        return reported_items
    else:
        return list()
