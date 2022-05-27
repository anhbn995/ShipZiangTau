import os
import pandas as pd


def append_new_row(csv_filepath, data_dict, use_index=False):
    if os.path.exists(csv_filepath):
        df = pd.read_csv(csv_filepath)
        new_df = pd.DataFrame(data=data_dict, columns=df.columns)
        with open(csv_filepath, 'a') as f:
            new_df.to_csv(f, header=False, index=use_index)
    else:
        new_df = pd.DataFrame(data=data_dict)
        new_df.to_csv(csv_filepath, index=use_index)
