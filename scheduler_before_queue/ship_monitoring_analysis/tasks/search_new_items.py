from ship_monitoring_analysis.api.planet_api import search


def search_all_items(api_key, aoi_geometry, date, item_type, asset_type):
    # get list of all items, compare to existed items, return new items
    all_item_info = search.search_downloadable_planet_scenes(api_key, aoi_geometry,
                                                             date, item_type=item_type, asset_type=asset_type)
    # check permission again before return list of items
    no_permission_items = []
    for item in all_item_info:
        permissions = item['_permissions']
        if not permissions:
            no_permission_items.append(item)
    permissive_item_info = [item for item in all_item_info if item not in no_permission_items]

    permissive_item_ids = [item['id'] for item in permissive_item_info]
    # all_item_ids = set(all_item_ids)
    # new_item_ids = all_item_ids - set(existed_item_ids)
    # new_item_ids = list(new_item_ids)
    # new_item_info = [item for item in permissive_items if item['id'] in new_item_ids]
    return permissive_item_ids, permissive_item_info
