import os
import pandas as pd
from ship_monitoring_analysis.detection_queue.queue import predict_task
from ship_monitoring_analysis.utils import csv_utils


def predict_new_items(item_ids, output_folder, aoi_file, mask_file, detection_date,
                      output_extension='.geojson', downloaded_file='downloaded_items.csv',
                      prediction_summary_file='predicted_items.csv', accepted_file='accepted_items.csv'):

    downloaded_file_path = os.path.join(output_folder, downloaded_file)
    downloaded_df = pd.read_csv(downloaded_file_path)
    new_downloaded_df = downloaded_df[downloaded_df['item_id'].isin(item_ids)]
    prediction_summary_file_path = os.path.join(output_folder, prediction_summary_file)
    accepted_file_path = os.path.join(output_folder, accepted_file)
    for index, row in new_downloaded_df.iterrows():
        item_id = row['item_id']
        item_path = row['downloaded_file']
        output_path = os.path.join(output_folder, item_id + output_extension)
        new_task = predict_task.apply_async(
            kwargs={
                'image_id': item_id,
                'image_path': item_path,
                'output_path': output_path,
                'aoi_file': aoi_file,
                'mask_file': mask_file,
                'detection_date': detection_date,
                'prediction_summary_file': prediction_summary_file_path
            }
        )
        print('task_id:', new_task.id)
        # TODO save item to accepted_items.csv
        csv_utils.append_new_row(accepted_file_path, {'item_id': [item_id]})
