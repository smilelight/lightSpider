import os
import time
import multiprocessing
from multiprocessing import Process, Queue, Manager

from lightutils import logger, send_email_notification, time_convert
from .writer import json_writer, csv_writer


class Spider:
    def __init__(self, base_url, save_format, save_path, proxy=None, interval=0):
        self.base_url = base_url
        if save_format == 'json':
            writer = json_writer
        elif save_format == 'csv':
            writer = csv_writer
        else:
            raise Exception('the writer save_format must be json or csv!')
        self.save_format = save_format
        self.writer = writer
        if not os.path.isdir(save_path):
            logger.warning('指定目录不存在！将创建存储目录{}'.format(save_path))
            os.mkdir(save_path)
        self.save_path = save_path
        self._parser = None
        self.proxy = proxy
        self.interval = interval

    def run(self, tasks, parser, notification=None):
        if type(tasks[0]) == int:
            tasks = [str(task) for task in tasks]
        if not os.path.isfile(self.save_path + os.sep + 'task.txt'):
            with open(self.save_path + os.sep + 'task.txt', 'w', encoding='utf-8') as f:
                for task in tasks:
                    f.write(task + '\n')

        if os.path.isfile(self.save_path + os.sep + 'handled.txt'):
            with open(self.save_path + os.sep + 'handled.txt', encoding='utf-8') as f:
                handled_tasks = [word.strip() for word in f]
        else:
            handled_tasks = list()
        unhandled_tasks = set(tasks) - set(handled_tasks)
        logger.info('已处理{}条数据，还需处理{}条数据'.format(len(handled_tasks), len(unhandled_tasks)))

        task_q = Queue()
        for task in unhandled_tasks:
            task_q.put(task)
        task_q.put('-end-')

        handled_tasks_list = Manager().list()

        result_q = Queue()
        result_process = Process(target=self.writer, args=(result_q, len(unhandled_tasks), self.save_path))
        result_process.start()

        begin_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info('开始爬取，当前时间为：{}'.format(begin_time))
        a = time.time()

        process_lst = []
        for i in range(multiprocessing.cpu_count()):
            p = Process(target=parser,
                        args=(self.base_url, task_q, result_q, handled_tasks_list, self.proxy, self.interval))
            process_lst.append(p)

        for p in process_lst:
            p.start()

        for p in process_lst:
            p.join()

        result_q.put(('-end-', None))
        result_process.join()

        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info('执行结束, 当前时间为：{}'.format(end_time))
        b = time.time()
        logger.info('本次共计耗时{}，共爬取{}条数据，平均速度为：{}(task/s)'.format(time_convert(round(b - a, 2)),
                                                                  len(unhandled_tasks),
                                                                  round(len(unhandled_tasks) / (b - a), 2)))
        if notification:
            if "to" not in notification or "task_name" not in notification:
                logger.info("the notification must have 'to' and 'task_name' attribute")
            else:
                result = send_email_notification(to=notification["to"],
                                                 subject="the spider job {} completed".format(
                                                     notification["task_name"]),
                                                 contents=["本次任务开始时间：{}".format(begin_time),
                                                           "本次任务结束时间：{}".format(end_time),
                                                           "写入文件夹：{}".format(self.save_path),
                                                           "保存文件格式：{}".format(self.save_format),
                                                           '本次共计耗时{}，共爬取{}条数据，平均速度为：{}(task/s)'.format(
                                                        time_convert(round(b - a, 2)), len(unhandled_tasks),
                                                        round(len(unhandled_tasks) / (b - a), 2))])
                if result:
                    logger.info("邮件发送成功！")
                else:
                    logger.info("邮件发送失败，看来是哪里出了差错，是否信息填写正确呢？")
