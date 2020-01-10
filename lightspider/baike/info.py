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
    result = {}
    if html.xpath('//div[@class="sorryBox"]'):  # 没有直接对应条目，还需进一步操作
        result['tag'] = 'none'
    else:
        result['info'] = {}
        if html.xpath('//div[@class="polysemant-list polysemant-list-normal"]'):  # 为多义词，且展示为最常用义项
            result['tag'] = 'multiple'

            # 获取基本信息
            title = html.xpath('string(//dd[@class="lemmaWgt-lemmaTitle-title"]/h1)')
            sub_title = html.xpath('string(//dd[@class="lemmaWgt-lemmaTitle-title"]/h2)')
            description = re.sub('\\n\[\d+(-\d+)?\]\\xa0\\n', '',
                                 html.xpath('string(//div[@class="lemma-summary"])')).strip()
            result['info']['word'] = title
            result['info']['basic'] = {
                'title': title,
                'sub_title': sub_title,
                'description': description
            }

            # 获取多个义项
            means = []
            for item in html.xpath('//div[@class="polysemant-list polysemant-list-normal"]//li'):
                if item.xpath('.//span'):
                    means.append((item.xpath('.//span/text()')[0],
                                  clean_word(response.url.replace(baike_url, ''))))
                else:
                    means.append((item.xpath('.//a/@title')[0],
                                  clean_word(item.xpath('.//a/@href')[0])))
            result['info']['means'] = means

            # 获取infobox信息
            if html.xpath('//div[@class="basic-info cmn-clearfix"]'):
                attrs = {}
                pros = html.xpath('//div[@class="basic-info cmn-clearfix"]//dt')
                for pro in pros:
                    attrs[clean_word(pro.xpath('string(.)'))] = \
                        clean_word(pro.xpath('string(.//following-sibling::*[1])'))
                result['info']['attrs'] = attrs

        elif html.xpath('//ul[@class="custom_dot  para-list list-paddingleft-1"]'):  # 为多义词，但展示为消岐页
            result['tag'] = 'ambiguous'
            title = html.xpath('string(//dd[@class="lemmaWgt-lemmaTitle-title"]/h1)')
            result['info']['word'] = title
            means = []
            for x in html.xpath('//ul[@class="custom_dot  para-list list-paddingleft-1"]//a'):
                means.append((x.xpath('string(.)'), clean_word(x.xpath('string(./@href)'))))
            result['info']['means'] = means

        else:  # 为单义词
            result['tag'] = 'signal'
            title = html.xpath('string(//dd[@class="lemmaWgt-lemmaTitle-title"]/h1)')
            description = re.sub('\\n\[\d+(-\d+)?\]\\xa0\\n', '',
                                 html.xpath('string(//div[@class="lemma-summary"])')).strip()
            result['info']['word'] = title
            result['info']['basic'] = {
                'title': title,
                'description': description
            }

            # 获取infobox信息
            if html.xpath('//div[@class="basic-info cmn-clearfix"]'):
                attrs = {}
                pros = html.xpath('//div[@class="basic-info cmn-clearfix"]//dt')
                for pro in pros:
                    attrs[clean_word(pro.xpath('string(.)'))] = \
                        clean_word(pro.xpath('string(.//following-sibling::*[1])'))
                result['info']['attrs'] = attrs

    return result
