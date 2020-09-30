# -*- coding: utf-8 -*-
# @Time    : 2020/2/22 21:04
# @Author  : lightsmile
# @Software: PyCharm

from lightspider import Spider, light, get_response, download_image, DEFAULT_PROXY
from lxml import etree
from lightutils import logger

local_path = r'D:\Data\KG\three_kingdoms'


@light
def parser(response):
    html = etree.HTML(response.text)
    post_list = html.xpath('//div[@id="postlist"]')[0]
    pic_infos = []
    items = post_list.xpath('./div')
    for item in items:
        if not item.xpath('.//img/@original'):
            detail_url = item.xpath('.//a/@href')[0]
            detail_res = get_response(detail_url)
            detail_html = etree.HTML(detail_res.text)
            pic_title = detail_html.xpath('//h2/text()')[0]
            pic_url = detail_html.xpath('//div[@class="main-body"]//img/@src')[0]
        else:
            pic_url = item.xpath('.//img/@original')[0]
            pic_title = item.xpath('.//span[@class="bg"]/text()')[0]
        # result = download_image(pic_url, local_path=local_path, name=pic_title)
        # logger.info('{}, {}, {}'.format(pic_title, pic_url, result))
        pic_infos.append((pic_title,
                          pic_url))

    return {
        'pic_infos': pic_infos,
        'url': response.url
    }, None


base_url = 'http://www.w3guo.com/pic/renwu{}'
tasks = ['']
for i in range(2, 128):
    tasks.append('/page/{}'.format(i))

save_format = 'json'
save_path = r'D:\Data\KG\three_kingdoms_pic'

proxy = {'http': '127.0.0.1:1080'}
spider = Spider(base_url=base_url, save_format=save_format, save_path=save_path, interval=2)


if __name__ == '__main__':
    spider.run(tasks, parser)
