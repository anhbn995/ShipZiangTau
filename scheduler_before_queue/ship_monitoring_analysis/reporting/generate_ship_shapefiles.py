import os
import zipfile
import subprocess


def generate_ship_shapefiles(item_dict, delivery_folder, output_zip_file, execute_path=None):
    # convert geojson to shapefile and zip
    shp_file_folders = []
    for item_id in item_dict.keys():
        geojson_file = item_dict[item_id]['result_path']
        output_shp_file = os.path.join(delivery_folder, item_id)
        if execute_path:
            ogr2ogr_path = os.path.join(execute_path, 'ogr2ogr')
        else:
            ogr2ogr_path = 'ogr2ogr'
        params = [ogr2ogr_path, '-f', 'ESRI Shapefile', output_shp_file, geojson_file]
        p = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        output, err = p.communicate()
        shp_file_folders.append(output_shp_file)
    with zipfile.ZipFile(output_zip_file, 'w') as myzip:
        for f in shp_file_folders:
            basename = os.path.basename(f)
            for root, dirs, files in os.walk(f):
                for file in files:
                    myzip.write(os.path.join(root, file), basename + '/' + file)
