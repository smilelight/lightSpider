# -*- coding: utf-8 -*-
# @Time    : 2020/5/23 12:06
# @Author  : lightsmile
# @Software: PyCharm

import re
import json
import urllib.parse

from lxml import etree

from ..worker import light
from ..downloader import get_response

table_url = "https://baike.baidu.com/guanxi/jsondata?"
base_url = 'https://baike.baidu.com/item/{}'
baike_url = "http://baike.baidu.com/"

re_table_id_str = 'rs_(.*?)"'
re_table_id_cmp = re.compile(re_table_id_str)

re_table_info_str = 'var rsdataList = (.*?);'
re_table_info_cmp = re.compile(re_table_info_str)


def get_url(table_id):
    params = {
        'action': 'getViewLemmaData',
        'args': [0, 8, {"fentryTableId": table_id, "lemmaId": 0, "subLemmaId": 0}, False]  # 8966513
    }

    url = table_url + urllib.parse.urlencode(params)
    return url


def query(query_url, use_base_url=True, use_proxy=False):
    res = []
    if use_base_url:
        query_url = base_url.format(query_url)
    response = get_response(query_url, use_proxy)
    table_ids = re_table_id_cmp.findall(response.text)
    if table_ids:
        table_infos = json.loads(re_table_info_cmp.findall(response.text)[0])['foot']
        # print(table_ids)
        # print(table_infos)
        assert len(table_infos) == len(table_ids)
        for info, table_id in zip(table_infos, table_ids):
            if info['isManual']:
                continue  # examples: '酶', 得到三个结果，但是html页面只展示2个，另外一个的isManual属性为1，一般为0，这里把它省略去
            else:
                table_title = info['fentryTableName']
            chunk = table_id.split('_')
            assert len(chunk) == 2
            res.append((table_title, int(chunk[1])))
    return res


def get_table(table_id, use_proxy=False):
    url = get_url(table_id)
    response = get_response(url, use_proxy)
    return _parse(response)


@light
def parser(response):
    return _parse(response), None


def _parse(response):
    res = dict()
    res['title'] = response.json()['title']
    res['items'] = []
    html = etree.HTML(response.json()['html'].replace('\r\n', ''))
    td = html.xpath('//td')
    for item in td:
        if item.xpath('.//td'):
            # print(item.xpath('string(.//th)'))
            continue
        if item.xpath('string(.)'):
            # print(item.xpath('string(.)').replace('▪', ''))
            # print(item.xpath('.//text()'))
            assert len(item.xpath('.//a')) == 1
            # print(item.xpath('string(.//a/@href)').replace(baike_url, ''))
            res['items'].append((item.xpath('string(.)').replace('▪', ''),
                                 item.xpath('string(.//a/@href)').replace(baike_url, '')))
    return res
