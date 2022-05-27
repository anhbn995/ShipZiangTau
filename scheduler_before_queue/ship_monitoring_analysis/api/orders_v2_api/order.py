import json
import requests


ORDERS_V2_API_URL = 'https://api.planet.com/compute/ops/orders/v2'


def parse_product(id_list, item_type, product_bundle):
    product = {
        'item_ids': id_list,
        'item_type': item_type,
        'product_bundle': product_bundle
    }
    return product


def parse_clip_tool(aoi_geometry):
    clip = {
        "clip": {
            "aoi": aoi_geometry
        }
    }
    return clip


def parse_parameters(name, products, tools, order_type, subscription_id=None):
    payload = {
        "name": name,
        "order_type": order_type,
        "products": products,
        "tools": tools,
    }
    if subscription_id:
        payload.update(subscription_id=subscription_id)
    return payload


def single_order(api_key, name, aoi_geometry, id_list, item_type='PSScene3Band', bundle='visual', order_type='full'):
    product = parse_product(id_list, item_type, bundle)
    clip = parse_clip_tool(aoi_geometry)
    order_payload = parse_parameters(name, [product], [clip], order_type)
    order_payload = json.dumps(order_payload)
    print(order_payload)

    headers = {'content-type': 'application/json',
               'cache-control': 'no-cache'}
    response = requests.request('POST', ORDERS_V2_API_URL, data=order_payload, headers=headers,
                                auth=(api_key, ''))
    if response.status_code == 202:
        content = response.json()
        order_id = content['id']
        order_url = content['_links']['_self']
        return order_id, order_url

    elif response.status_code == 400:
        raise Exception('Failed with response: Bad request', response.text)
    elif response.status_code == 401:
        raise Exception('Failed with response: Forbidden', response.text)
    elif response.status_code == 409:
        raise Exception('Failed with response: MaxConcurrency', response.text)
    else:
        raise Exception('Unrecognized status code.', response.text)


if __name__ == '__main__':
    api_key = 'e223ca1e2d7840fe8a886f6bde758029'
    order_name = 'test-order'
    _id_list = ['20190801_181253_1024', '20190801_181252_1024']
    _item_type = 'PSScene3Band'
    _bundle_type = 'visual'
    _order_type = 'partial'
    _aoi_file = '/media/giangblackk/Data0/skymapdev/indonesia_ship/code/scheduler-before-queue/scheduler-before-queue/tmp/aoi/AOI_LA_FeatureCollection.geojson'
    with open(_aoi_file, 'r') as f:
        _aoi = json.load(f)
        if 'type' in _aoi:
            if _aoi['type'] == 'FeatureCollection':
                _aoi_geometry = _aoi['features'][0]['geometry']
            elif _aoi['type'] == 'Feature':
                _aoi_geometry = _aoi['geometry']
            elif _aoi['type'] == 'Polygon':
                _aoi_geometry = _aoi
            else:
                raise Exception('Invalid GeoJSON file', _aoi)
        else:
            raise Exception('Invalid GeoJSON file', _aoi)

    _order_id, _order_url = single_order(api_key, order_name, _aoi_geometry, _id_list, _item_type, _bundle_type, _order_type)
    print(_order_id, _order_url)
