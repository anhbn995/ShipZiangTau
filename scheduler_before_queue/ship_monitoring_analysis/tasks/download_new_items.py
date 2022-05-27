import os
from ship_monitoring_analysis.api.planet_api import download, search
from ship_monitoring_analysis.api.planet_api import scene_download
from ship_monitoring_analysis.api.orders_v2_api import clip_and_ship, asset_bundle_map
from ship_monitoring_analysis.utils import misc


def download_new_items(api_key, aoi_geometry, item_ids, item_type, asset_type, base_folder, execute_path,
                       use_clip_and_ship=False, download_alter_tile_image=False, zoom_level=15):
    # download items
    if use_clip_and_ship:
        # download using clip and ship api
        bundle_type = asset_bundle_map.ASSET_BUNDLE_MAPPING[item_type]['assets'][asset_type]['bundle']
        successful_items_dict = {}
        item_format = search.DOWNLOAD_FILE_FORMAT[item_type][asset_type]
        item_format = item_format.replace('.tif', '_clip.tif')
        item_format = os.path.join(base_folder, item_format)

        clip_and_ship.download_clip_scenes(api_key, 'default', aoi_geometry, item_ids, base_folder, item_type, bundle_type)
        for item_id in item_ids:
            corresponding_item_file = item_format.format(item_id=item_id)
            successful_items_dict[item_id] = corresponding_item_file
    else:
        if download_alter_tile_image:
            successful_items_dict = {}
            item_format = search.DOWNLOAD_FILE_FORMAT[item_type][asset_type]
            item_format = os.path.join(base_folder, item_format)
            scene_download.download_scene_tiles(api_key, item_ids, item_format, zoom_level=zoom_level, item_type=item_type)
            for item_id in item_ids:
                corresponding_item_file = item_format.format(item_id=item_id)
                successful_items_dict[item_id] = corresponding_item_file
        else:
            download.download_scenes(api_key, item_ids, base_folder, item_type, asset_type, execute_path=execute_path)
            successful_items_dict = {}
            # check downloaded items
            for item_id in item_ids:
                corresponding_item_file = search.DOWNLOAD_FILE_FORMAT[item_type][asset_type].format(item_id=item_id)
                corresponding_item_file = os.path.join(base_folder, corresponding_item_file)
                if os.path.exists(corresponding_item_file):
                    # get md5_digest
                    planet_md5_digest = search.get_asset_md5_digest(api_key, item_id)
                    local_md5_digest = misc.md5sum(corresponding_item_file)
                    if local_md5_digest == planet_md5_digest:
                        successful_items_dict[item_id] = corresponding_item_file
                    else:
                        print(local_md5_digest, planet_md5_digest)
                else:
                    print(corresponding_item_file)
    return successful_items_dict
