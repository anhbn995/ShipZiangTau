import os
import pandas as pd


def get_accepted_items(data_folder, accepted_items_file='accepted_items.csv', column_name='item_id'):
    accepted_items_file_path = os.path.join(data_folder, accepted_items_file)
    if os.path.exists(accepted_items_file_path):
        df = pd.read_csv(accepted_items_file_path)
        accepted_items = df[column_name].tolist()
        return accepted_items
    else:
        return list()
