from urllib.parse import unquote

from lxml import etree

from ..worker import light
from ..downloader import get_response

base_url = 'https://baike.baidu.com/search/none?word={}&pn=0&rn=10&enc=utf8'
save_format = 'json'
baike_url = 'https://baike.baidu.com'


def clean_search_word(word):
    return unquote(word).strip().replace('https://baike.baidu.com', '').replace('/item/', '')


@light
def parser(response):
    return _parse(response), None


def query(word, use_proxy=False):
    url = base_url.format(word)
    response = get_response(url, use_proxy)
    return _parse(response)


def _parse(response):
    html = etree.HTML(response.text)
    result = {}
    if html.xpath('//div[@class="no-result"]'):
        result['search_word'] = html.xpath('string(//div[@class="no-result"]//em)')
        result['result'] = []
    else:
        result['search_word'] = html.xpath('string(//dl[@class="search-list"]//dt/em)')
        result['result'] = []
        for item in html.xpath('//dl[@class="search-list"]//dd'):
            result['result'].append({
                'title': item.xpath('string(./a)'),
                'url': clean_search_word(item.xpath('string(./a/@href)')),
                'description': item.xpath('string(./p)'),
                'result_date': item.xpath('string(./span)')
            })
    return result
