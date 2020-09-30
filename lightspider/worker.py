import time
from functools import wraps
from .downloader import get_response


def light(parser):
    @wraps(parser)
    def worker(base_url, task_q, result_q, handled_tasks_list, proxy=None, interval=0):
        while True:
            task = task_q.get(True)
            if task == '-end-':
                task_q.put(task)
                break
            if task in handled_tasks_list:
                continue
            try:
                response = get_response(base_url.format(task), proxy)
                if response:
                    info, tasks = parser(response)
                else:
                    info, tasks = None, None
            except Exception as e:
                print(e)
                task_q.put(task)
                continue
            if info:
                result_q.put((info, task))
                handled_tasks_list.append(task)
                if tasks:
                    for task in tasks:
                        task_q.put(task)
            else:
                task_q.put(task)
            time.sleep(interval)  # 默认休眠1s，一方面减少ip被封风险，一方面不给服务器造成太大负担
    return worker
