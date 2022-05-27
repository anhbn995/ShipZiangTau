import datetime

from planet import api
from planet.api import filters

ASSERT_TYPES = {
    'PSScene3Band':
        [
            'analytic',
            'analytic_dn',
            'analytic_dn_xml',
            'analytic_xml',
            'basic_analytic',
            'basic_analytic_dn',
            'basic_analytic_dn_rpc',
            'basic_analytic_dn_xml',
            'basic_analytic_rpc',
            'basic_analytic_xml',
            'basic_udm',
            'udm',
            'visual',
            'visual_xml',
        ],
    'SkySatScene':
        [
            'analytic',
            'basic_analytic',
            'basic_analytic_dn',
            'basic_analytic_dn_rpc',
            'basic_panchromatic_dn',
            'basic_panchromatic_dn_rpc',
            'ortho_analytic_dn',
            'ortho_analytic_udm',
            'ortho_panchromatic_dn',
            'ortho_panchromatic_udm',
            'ortho_pansharpened',
            'ortho_pansharpened_udm',
            'ortho_visual',
        ]
}

DOWNLOAD_FILE_FORMAT = {
    'PSScene3Band':
        {
            'visual': '{item_id}_3B_Visual.tif',
            'analytic': '{item_id}_3B_Analytic.tif'
        },
    'SkySatScene':
        {
            'ortho_visual': '{item_id}_visual.tif'
        }
}


def get_asset_md5_digest(api_key, item_id, item_type='PSScene3Band', asset_type='visual'):
    client = api.ClientV1(api_key=api_key)
    item = client.get_item(item_type=item_type, id=item_id).get()
    assets = client.get_assets(item).get()
    asset = assets[asset_type]
    md5_digest = asset['md5_digest']
    return md5_digest


def search_planet_scenes(api_key, aoi_geometry, start_date, date_range=1, item_type='PSScene3Band'):
    # create client
    client = api.ClientV1(api_key=api_key)

    # create date range filter
    end_date = start_date + datetime.timedelta(days=date_range)

    date_filter = filters.date_range('acquired',
                                     gt=start_date.strftime(format('%Y-%m-%d')),
                                     lt=end_date.strftime(format('%Y-%m-%d')))

    # create simple filter
    query = filters.and_filter(
        filters.geom_filter(aoi_geometry),
        date_filter)

    # search all items filtered by geometry and date range
    simple_request = filters.build_search_request(query, item_types=[item_type])
    simple_result = client.quick_search(simple_request)

    all_items = [item for item in simple_result.items_iter(limit=None)]
    return all_items


def search_downloadable_planet_scenes(api_key, aoi_geometry, start_date, date_range=1, item_type='PSScene3Band',
                                      asset_type='visual', cloud_cover_threshold=100):
    # check download type
    assert item_type in ASSERT_TYPES, 'the item type is not valid: {}'.format(item_type)
    assert asset_type in ASSERT_TYPES[item_type], 'the asset type is not valid: {}'.format(asset_type)
    permission_type = 'assets.{}:download'.format(asset_type)

    # create client
    client = api.ClientV1(api_key=api_key)

    # create date range filter
    end_date = start_date + datetime.timedelta(days=date_range)

    date_filter = filters.date_range('acquired',
                                     gt=start_date.strftime(format('%Y-%m-%d')),
                                     lt=end_date.strftime(format('%Y-%m-%d')))

    # create query to search downloadable items (using Planet API)
    query = filters.and_filter(
        filters.geom_filter(aoi_geometry),
        date_filter,
        filters.range_filter('cloud_cover', lt=cloud_cover_threshold),
        filters.permission_filter(permission_type),
    )

    request = filters.build_search_request(
        query, item_types=[item_type]
    )

    result = client.quick_search(request)

    downloadable_items = [item for item in result.items_iter(limit=None)]
    return downloadable_items
