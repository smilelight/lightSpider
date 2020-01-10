from lightspider.baike import info
from lightspider import Spider


tasks = ['曹操', '曹操字孟德', '司马懿', '仐三',
         '自然语言处理', '知识图谱', '人工智能', '深度学习', '爬虫', 'Python', 'Pytorch', '曹操']

spider = Spider(base_url=info.base_url, format=info.save_format, save_path=r'D:\Data\NLP\corpus\baike_info')

if __name__ == '__main__':
    spider.run(tasks, info.parser)
