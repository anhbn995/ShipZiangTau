from ship_monitoring_analysis.api.orders_v2_api import order, downloader


def download_clip_scenes(api_key, order_name, aoi_geometry, item_ids, output_folder, item_type='PSScene3Band', bundle_type='visual'):
    if item_ids:
        order_id, order_url = order.single_order(api_key, order_name, aoi_geometry, item_ids, item_type, bundle_type)
        print('Order info:', order_id, order_url)
        downloader.download(api_key, order_url, output_folder, ext='.tif')
    else:
        print('Empty item list, no item to download')
