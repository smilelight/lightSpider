from lightspider.baike import href
from lightspider import Spider


tasks = ['曹操', '曹操字孟德']

spider = Spider(base_url=href.base_url, format=href.save_format, save_path=r'D:\Data\NLP\corpus\baike_href')

if __name__ == '__main__':
    spider.run(tasks, href.parser)
