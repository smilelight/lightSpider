from lightspider.baike import info
from lightspider import Spider

base_url = 'https://baike.baidu.com/view/{}.htm'
tasks = [x for x in range(100000, 1000000)]
save_format = 'json'

spider = Spider(base_url=base_url, format=save_format, save_path=r'D:\Data\NLP\corpus\baike_info_100000_to_1000000')

if __name__ == '__main__':
    spider.run(tasks, info.parser)
