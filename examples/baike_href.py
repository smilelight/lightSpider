from lightspider.baike import href
from lightspider import Spider


tasks = ['曹操', '曹操字孟德']

notification = {
    "to": "iamlightsmile@qq.com",
    "task_name": "baike_href"
}

spider = Spider(base_url=href.base_url, save_format=href.save_format, save_path=r'D:\Data\NLP\corpus\baike_href')

if __name__ == '__main__':
    spider.run(tasks, href.parser, notification)
