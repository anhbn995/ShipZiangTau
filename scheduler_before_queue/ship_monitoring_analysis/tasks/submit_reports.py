import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

REPORT_API_URL = 'https://ship-monitoring.imagetrekk.com/api/detection/reports'


def submit(aoi_name, publish_date, ship_detection_file, ship_summary_file, report_file):
    multipart_data = MultipartEncoder(
        fields={
            'ship_detection_file': (
            os.path.basename(ship_detection_file), open(ship_detection_file, 'rb'), 'application/zip'),
            'ship_detection_summary_file': (
            os.path.basename(ship_summary_file), open(ship_summary_file, 'rb'), 'text/csv'),
            'report_file': (os.path.basename(report_file), open(report_file, 'rb'), 'application/pdf'),
            'aoi': aoi_name,
            'publish_at': publish_date,
            'override': 'true'
        }
    )
    try:
        response = requests.post(REPORT_API_URL, data=multipart_data,
                             headers={'Content-Type': multipart_data.content_type},verify=False)
        print('-------------------------- DEBUG /api/detection/reports RESPONSE -------------------------------')
        print(response.content)

        return response
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('-------------------------- DEBUG /api/detection/reports ERROR -------------------------------')
        print(e)


def submit_report(aoi_name, publish_date, csv_file, report_file, zip_file):
    response = submit(aoi_name.replace('_', ' '), publish_date.strftime('%Y-%m-%d'), zip_file, csv_file, report_file)
