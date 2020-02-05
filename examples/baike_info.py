from lightspider.baike import info
from lightspider import Spider


tasks = ['曹操', '曹操字孟德', '司马懿',
         '自然语言处理', '知识图谱', '人工智能', '深度学习', '爬虫']

notification = {
    "to": "iamlightsmile@qq.com",
    "task_name": "baike_info"
}

spider = Spider(base_url=info.base_url, save_format=info.save_format, save_path=r'D:\Data\NLP\corpus\baike_info')

if __name__ == '__main__':
    spider.run(tasks, info.parser, notification=notification)
