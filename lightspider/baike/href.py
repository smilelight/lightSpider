import re
from urllib.parse import unquote

from lxml import etree

from ..worker import light
from ..downloader import get_response

base_url = 'https://baike.baidu.com/item/{}'
save_format = 'json'
baike_url = 'https://baike.baidu.com'


def clean_word(word):
    return re.sub('\[\d+(-\d+)?\]', '',
                  re.sub('\s', '', unquote(word))).strip().replace('#viewPageContent', '').replace('/item/', '')


@light
def parser(response):
    return _parse(response), None


def query(word, use_proxy=False):
    url = base_url.format(word)
    response = get_response(url, use_proxy)
    return _parse(response)


def _parse(response):
    html = etree.HTML(response.text)
    if html.xpath('//div[@class="sorryBox"]'):  # 没有直接对应条目，还需进一步操作
        links = []
        title = None
    else:
        title = clean_word(response.url.replace(baike_url, ''))
        hrefs = [x for x in html.xpath('//a') if
                 x.xpath('string(.)').strip() and x.xpath('./@href') and x.xpath('./@href')[0].startswith('/item')]
        links = []
        for href in hrefs[5:-1]:  # [5:-1]是因为去掉了无关item项
            # title = href.xpath('string(.)').strip()
            link = clean_word(href.xpath('string(./@href)'))
            links.append(link)
    return {
        'title': title,
        'links': links
    }
