# -*- coding: utf-8 -*-
# @Time    : 2020/2/23 9:53
# @Author  : lightsmile
# @Software: PyCharm

from lightspider import Spider, light
from lxml import etree


@light
def parser(response):
    html = etree.HTML(response.text)
    title = html.xpath('string(.//div[@class="list-group-item active-cat"])').strip()
    items = html.xpath('.//div[@id="ipt-kb-affix-active-post"]/a')
    items = [(item.xpath('string(.)').strip(), item.xpath('string(./@href)'))for item in items]
    return {
        'category': title,
        'peoples': items
    }, None


base_url = 'http://www.w3guo.com/wiki/hero/{}'
tasks = ['other', 'wu', 'wei', 'shu', 'jin']

save_format = 'json'
save_path = r'D:\Data\KG\three_kingdoms_people'

spider = Spider(base_url=base_url, save_format=save_format, save_path=save_path, interval=2)

if __name__ == '__main__':
    spider.run(tasks, parser)
