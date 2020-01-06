import os, time
import multiprocessing
from multiprocessing import Process, Queue

from lightspider.utils.log import logger
from lightspider.writer import json_writer, csv_writer


class Spider:
    def __init__(self, base_url, style, save_path):
        self.base_url = base_url
        if style == 'json':
            writer = json_writer
        elif style == 'csv':
            writer = csv_writer
        else:
            raise Exception('the writer style must be json or csv!')
        self.style = style
        self.writer = writer
        if not os.path.isdir(save_path):
            logger.warning('指定目录不存在！将创建存储目录{}'.format(save_path))
            os.mkdir(save_path)
        self.save_path = save_path

    def run(self, tasks, handler):
        if type(tasks[0]) == int:
            tasks = [str(task) for task in tasks]
        if not os.path.isfile(self.save_path + '/task.txt'):
            with open(self.save_path + '/task.txt', 'w', encoding='utf-8') as f:
                for task in tasks:
                    f.write(task + '\n')

        if os.path.isfile(self.save_path + '/handled.txt'):
            with open(self.save_path + '/handled.txt', encoding='utf-8') as f:
                handled_tasks = [word.strip() for word in f]
        else:
            handled_tasks = list()
        unhandled_tasks = set(tasks) - set(handled_tasks)
        logger.info('已处理{}条数据，还需处理{}条数据'.format(len(handled_tasks), len(unhandled_tasks)))

        task_q = Queue()
        for task in unhandled_tasks:
            task_q.put(task)
        task_q.put('-end-')

        result_q = Queue()
        result_process = Process(target=self.writer, args=(result_q, len(unhandled_tasks), self.save_path))
        result_process.start()

        logger.info('开始爬取，当前时间为：{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        a = time.time()

        process_lst = []
        for i in range(multiprocessing.cpu_count()):
            p = Process(target=handler, args=(self.base_url, task_q, result_q))
            process_lst.append(p)

        for p in process_lst:
            p.start()

        for p in process_lst:
            p.join()

        result_q.put(('-end-', None))
        result_process.join()

        logger.info('执行结束, 当前时间为：{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        b = time.time()
        logger.info('本次共计耗时{}s，共爬取数据条数为{}，平均速度为：{}(task/s)'.format(round(b - a, 2), len(unhandled_tasks),
                                                                 round(len(unhandled_tasks) / (b - a), 2)))
