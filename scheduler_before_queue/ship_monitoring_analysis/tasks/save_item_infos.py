import os
import pandas as pd
import json


def save_item_info(downloaded_items_dict, item_info, output_folder, output_filename='downloaded_items.csv',
                   id_col_name='item_id', file_col_name='downloaded_file', info_col_name='item_info', use_index=False):
    total_info = []
    for item in item_info:
        item_id = item['id']
        item_compressed_info = json.dumps(item)
        downloaded_item_file = downloaded_items_dict[item_id]
        new_item = {id_col_name: item_id, file_col_name: downloaded_item_file, info_col_name: item_compressed_info}
        total_info.append(new_item)

    output_filepath = os.path.join(output_folder, output_filename)

    if os.path.exists(output_filepath):
        df = pd.read_csv(output_filepath)
        new_df = pd.DataFrame(data=total_info, columns=df.columns)
        with open(output_filepath, 'a') as f:
            new_df.to_csv(f, header=False, index=use_index)
    else:
        new_df = pd.DataFrame(data=total_info, columns=[id_col_name, file_col_name, info_col_name])
        new_df.to_csv(output_filepath, index=use_index)
