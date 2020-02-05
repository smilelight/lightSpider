from lightspider.baike import href
from lightspider import Spider


base_url = 'https://baike.baidu.com/view/{}.htm'
tasks = [x for x in range(2000000, 3000000)]
save_format = 'json'

notification = {
    "to": "iamlightsmile@qq.com",
    "task_name": "baike_href"
}

spider = Spider(base_url=base_url, save_format=save_format,
                save_path=r'D:\Data\NLP\corpus\baike_href_2000000_to_3000000')

if __name__ == '__main__':
    spider.run(tasks, href.parser, notification=notification)
