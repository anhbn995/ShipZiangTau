import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import pandas as pd
import json

SHIP_API_URL = 'https://ship-monitoring.imagetrekk.com/api/detection/ships'


def submit(image_id, result_file, acquired_datetime, aoi_name, overwrite=True):
    result_filename = os.path.basename(result_file)
    fields = {
        # a file upload field
        'geojson': (result_filename, open(result_file, 'rb'), 'text/plain'),
        # plain text fields+
        'api_key': '94w1a37aed9461a847edd79a2e4201b',
        'planet_image_id': image_id,
        'planet_image_source': '3-band (RGB) PlanetScope imagery that is framed as captured',
        'detect_type': 'daily_ship_detection',
        'replace_existed': 'true' if overwrite else 'false',
        'image_date': acquired_datetime,
        'detect_date': acquired_datetime,
        'aoi_name': aoi_name
    }
    print(fields)
    multipart_data = MultipartEncoder(fields=fields)
    try:
        response = requests.post(SHIP_API_URL, data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type},verify=False)
        
        print('-------------------------- DEBUG /api/detection/ships RESPONSE -------------------------------')
        print(response.content)
        
        return response
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('_________________ DEBUG DUCANH /api/detection/ships _________________')
        print(e)


def submit_ships(new_item_ids, aoi_name, data_folder,
                 downloaded_file='downloaded_items.csv', predicted_file='predicted_items.csv'):
    aoi_name = aoi_name.replace('_', ' ')
    # get all item information into 1 dict - predicted_item_info
    predicted_file_path = os.path.join(data_folder, predicted_file)
    downloaded_file_path = os.path.join(data_folder, downloaded_file)
    predicted_df = pd.read_csv(predicted_file_path)
    downloaded_df = pd.read_csv(downloaded_file_path)
    predicted_item_info = {}
    for index, row in predicted_df.iterrows():
        item_id = row['item_id']
        result_file_path = row['result_path']
        if item_id in new_item_ids:
            predicted_item_info[item_id] = {'result_path': result_file_path}
    for index, row in downloaded_df.iterrows():
        item_id = row['item_id']
        item_downloaded_file = row['downloaded_file']
        item_info = row['item_info']
        item_info = json.loads(item_info)
        if item_id in predicted_item_info:
            predicted_item_info[item_id].update(downloaded_file=item_downloaded_file, item_info=item_info)
    for item_id, item_info in predicted_item_info.items():
        acquired_datetime = item_info['item_info']['properties']['acquired']
        ship_file = item_info['result_path']
        print(item_id, ship_file, acquired_datetime, aoi_name)
        response = submit(item_id, ship_file, acquired_datetime, aoi_name)

