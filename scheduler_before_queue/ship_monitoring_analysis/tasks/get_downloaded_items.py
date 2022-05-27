import os
import pandas as pd


def get_downloaded_items(output_folder, output_filename='downloaded_items.csv', column_name='item_id'):
    output_filepath = os.path.join(output_folder, output_filename)
    if os.path.exists(output_filepath):
        df = pd.read_csv(output_filepath)
        item_ids = df[column_name].tolist()
        return item_ids
    else:
        return []
