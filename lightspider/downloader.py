import os

import requests
from lightutils import logger

from .utils.proxy import get_proxy, DEFAULT_PROXY

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36'
}


def get_response(url, user_proxy=None):
    if user_proxy:
        if user_proxy == DEFAULT_PROXY:
            proxy = get_proxy()
            if proxy:
                proxy = {
                    'http': proxy
                }
        else:
            proxy = user_proxy
    else:
        proxy = None
    try:
        r = requests.get(url, headers=HEADERS, proxies=proxy, timeout=3)
        if r.status_code == requests.codes.ok:
            if r.encoding != 'utf-8':
                r.encoding = 'utf-8'
            return r
    except Exception as e:
        logger.info(str(e))
        return None
    return None


def download_image(url: str, local_path: str, name=None, override=True):
    if not url.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']:
        return False
    try:
        image = requests.get(url, headers=HEADERS, timeout=3)
        if image.status_code != 200:
            return False
        else:
            file_name = url.split('/')[-1]
            if name:
                file_name = name + '.' + file_name.split('.')[-1]
            file_path = local_path + os.sep + file_name
            if os.path.isfile(local_path + os.sep + file_name) and not override:
                return False
            else:
                open(file_path, 'wb').write(image.content)
                return True
    except Exception as e:
        return False
