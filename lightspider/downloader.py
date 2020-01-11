import requests

from .utils.proxy import get_proxy, DEFAULT_PROXY


def get_response(url, user_proxy=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36'
    }
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
    r = requests.get(url, headers=headers, proxies=proxy, timeout=3)
    if r.status_code == requests.codes.ok:
        if r.encoding != 'utf-8':
            r.encoding = 'utf-8'
        return r
    return None
