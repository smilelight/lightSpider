from lightspider.baike import search
from lightspider import Spider


tasks = ['曹操', '曹操字孟德']

spider = Spider(base_url=search.base_url, save_format=search.save_format, save_path=r'D:\Data\NLP\corpus\baike_search')

if __name__ == '__main__':
    spider.run(tasks, search.parser)
