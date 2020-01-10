from lightspider import Spider
from lightspider import light

from lxml import etree
import re


# 编写页面解析函数
@light
def parser(response):
    """
    必要的页面解析函数
    :param response: 执行Request请求后得到的Response对象，可以自由选择xpath或BeautifulSoup等方式解析处理
    :return: type：tuple:(解析得到的数据对象, 解析页面得到的新的tasks（要么为List，要么为None)
    """
    html = etree.HTML(response.text)
    info = html.xpath('//div[@class="col-md-8"]')[0]
    words = [re.sub(r'\(\d+\)', '', item.xpath('string(.)')) for item in info.xpath('./b')[:-1]]
    mean = info.xpath('./a/text()')[0]
    return {
        'mean': mean,
        'words': words
    }, None

# 编写生成tasks脚本
# tasks = []
# base_url = 'https://www.cilin.org/jyc/b_{}.html'
# for i in range(1, 9996):
#     tasks.append(i)
#
# spider = Spider(base_url=base_url, style='json', save_path=r'D:\Data\NLP\corpus\jyc')


tasks = []
for i in range(1, 30):
    tasks.append(i)

base_url = 'https://www.cilin.org/jyc/b_{}.html'
save_format = 'json'

spider = Spider(base_url=base_url, format=save_format, save_path=r'D:\Data\NLP\corpus\test', use_proxy=True)


if __name__ == '__main__':
    spider.run(tasks, parser)
