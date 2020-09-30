import json

from lightspider import Spider, light, get_response
from lxml import etree


def clean_str(x):
    if isinstance(x, str):
        return x.strip()
    elif isinstance(x, list):
        return [item.strip() for item in x]


def extract(html):
    paras = html.xpath('./p|./h1|./h2|./h3|./h4|./h5|./ul|./ol|./figure|./div[@class="table-container"]')
    if not paras:
        return html.xpath('string(.)')
    result = []

    for para in paras:
        if para.xpath('name(.)') == 'p':
            if para.xpath('.//img'):
                result.append({
                    'type': 'img',
                    'href': para.xpath('string(.//img/@src)').strip()
                })
            elif para.xpath('.//figure'):
                result.append({
                    'type': 'p',
                    'text': '\n'.join(para.xpath('./text()'))
                })
                result.extend(extract(para))
            else:
                result.append({
                    'type': 'p',
                    'text': para.xpath('string(.)').strip()
                })
        elif para.xpath('name(.)') == 'figure':
            code_type = para.xpath('string(./@class)').split()[-1]
            code_lines = []
            for code_line in para.xpath('.//td[@class="code"]//span[@class="line"]'):
                code_lines.append(code_line.xpath('string(.)'))
            result.append({
                'type': 'code',
                'code': {
                    'type': code_type,
                    'source': '\n'.join(code_lines)
                }
            })
        elif para.xpath('string(./@class)') == 'table-container':
            headers = para.xpath('.//th/text()')
            rows = [x.xpath('.//td/text()') for x in para.xpath('.//tbody//tr')]
            result.append({
                'type': 'table',
                'table': {
                    'headers': headers,
                    'rows': rows
                }
            })
        elif para.xpath('name(.)') in ['ol', 'ul']:
            result.append({
                'type': para.xpath('name(.)'),
                'lis': [extract(x) for x in para.xpath('./li')]
            })
        else:
            result.append({
                'type': para.xpath('name(.)'),
                'text': para.xpath('string(.)').strip()
            })
    return result

@light
def parser(response):
    html = etree.HTML(response.text)
    title = clean_str(html.xpath('string(//h1[@class="title"])'))
    content = extract(html.xpath('//div[@class="article-entry"]')[0])
    created_time = clean_str(html.xpath('string(//div[@id="header-meta"]//time)'))
    categories = clean_str(html.xpath('//div[@id="header-meta"]//div[@class="metatag cats"]//a/text()'))
    latest_time = clean_str(html.xpath('string(//section[@id="footer-meta"]//time)'))
    tags = clean_str(html.xpath('//section[@id="footer-meta"]//div[@class="metatag tags"]//a/text()'))
    return {
        'title': title,
        'content': content,
        'created_time': created_time,
        'categories': categories,
        'latest_time': latest_time,
        'tags': tags,
        'url': response.url
    }, None


if __name__ == '__main__':
    base_url = r'http://www.lightsmile.cn{}'
    archives_url = r'http://www.lightsmile.cn/archives'
    archives_res = get_response(archives_url)
    archives_html = etree.HTML(archives_res.text)
    section = archives_html.xpath('//section[@class="archive"]')[0]
    archives = section.xpath('.//a')
    tasks = []
    for archive in archives:
        tasks.append(archive.xpath('string(./@href)'))
    save_format = 'json'

    spider = Spider(base_url=base_url, save_format=save_format, save_path=r'D:\Data\NLP\corpus\my_blogs_test')
    spider.run(tasks, parser)
    # test_url = base_url.format(tasks[39])
    # test_res = get_response(test_url)
    # test_result = parser(test_res)
    # print(test_result)
    # test_url = base_url.format(tasks[39])
    # test_res = get_response(test_url)
    # test_result = parser(test_res)
