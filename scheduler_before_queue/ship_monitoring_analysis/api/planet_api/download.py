import os
import subprocess


def download_scenes(api_key, item_ids, output_folder, item_type='PSScene3Band', asset_type='visual',
                    execute_path=None):

    assert isinstance(item_ids, list), 'item_ids must be a list'

    if item_ids:
        if execute_path:
            planet_tool_path = os.path.join(execute_path, 'planet')
        else:
            planet_tool_path = 'planet'
        params = [planet_tool_path, '--api-key', '{}'.format(api_key),
                  'data', 'download', '--item-type', item_type,
                  '--asset-type', asset_type,
                  '--string-in', 'id', ' '.join(item_ids),
                  '--dest', '{}'.format(output_folder)
                  ]
        p = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        output, err = p.communicate()
        return output, err
    else:
        return 'Empty item list, no item to download', ''
