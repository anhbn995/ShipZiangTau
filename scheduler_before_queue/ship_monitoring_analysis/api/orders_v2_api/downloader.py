import requests
import time
import progressbar
import os
import sys
from retrying import retry


# To get redirect link
@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000)
def check_for_redirects(session, url):
    try:
        r = session.get(url, allow_redirects=False, timeout=0.5)
        if 300 <= r.status_code < 400:
            return r.headers['location']
        elif r.status_code == 429:
            raise Exception("rate limit error")
    except requests.exceptions.Timeout:
        return '[timeout]'
    except requests.exceptions.ConnectionError:
        return '[connection error]'
    except requests.HTTPError as e:
        if r.status_code == 429:  # Too many requests
            raise Exception("rate limit error")


# Get the redirects and download
@retry(
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000)
def download_only(session, redirect_url, local_path, ext, items):
    result = session.get(redirect_url)
    if not os.path.exists(local_path) and result.status_code == 200:
        if ext is not None:
            if local_path.endswith(ext):
                print("Downloading: " + str(local_path))
                f = open(local_path, 'wb')
                for chunk in result.iter_content(chunk_size=512 * 1024):
                    if chunk:
                        f.write(chunk)
                f.close()
        elif ext is None:
            print("Downloading: " + str(local_path))
            f = open(local_path, 'wb')
            for chunk in result.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)
            f.close()
    elif result.status_code == 429:
        raise Exception("rate limit error")
    else:
        if int(result.status_code) != 200:
            print("Encountered error with code: " + str(result.status_code) + ' for ' + str(
                os.path.split(items['name'])[-1]))
        elif int(result.status_code) == 200:
            print("File already exists SKIPPING: " + str(os.path.split(items['name'])[-1]))


def download(api_key, url, local, ext):
    session = requests.Session()
    session.auth = (api_key,'')
    response = session.get(url).json()
    print("Polling ...")
    while response['state'] == 'running' or response['state'] == 'starting':
        bar = progressbar.ProgressBar()
        for z in bar(range(60)):
            time.sleep(1)
        response = session.get(url).json()
    if response['state'] == 'success' or response['state'] == 'partial':
        print('Order completed with status: ' + str(response['state']))
        for items in response['_links']['results']:
            url = (items['location'])
            url_to_check = url if url.startswith('https') else "http://%s" % url
            redirect_url = check_for_redirects(session, url_to_check)
            if redirect_url.startswith('https'):
                # print('Processing redirect link for '+str(os.path.split(items['name'])[-1]))
                local_path = os.path.join(local, str(os.path.split(items['name'])[-1]))
                try:
                    download_only(session, redirect_url, local_path, ext, items)
                except Exception as e:
                    print(e)
                except (KeyboardInterrupt, SystemExit) as e:
                    print('\n' + 'Program escaped by User')
                    sys.exit()
    else:
        print('Order Failed with state: ' + str(response['state']))
