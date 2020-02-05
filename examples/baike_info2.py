from lightspider.baike import info
from lightspider import Spider

base_url = 'https://baike.baidu.com/view/{}.htm'
tasks = [x for x in range(4000000, 5000000)]
save_format = 'json'

notification = {
    "to": "iamlightsmile@qq.com",
    "task_name": "baike_info"
}

spider = Spider(base_url=base_url, save_format=save_format,
                save_path=r'D:\Data\NLP\corpus\baike_info_4000000_to_5000000')

if __name__ == '__main__':
    spider.run(tasks, info.parser, notification=notification)
