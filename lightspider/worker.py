import time
from functools import wraps
from .downloader import get_page


def light(handler):
    @wraps(handler)
    def worker(base_url, task_q, result_q):
        while True:
            task = task_q.get(True)
            if task == '-end-':
                task_q.put(task)
                break
            try:
                page = get_page(base_url.format(task))
                if page:
                    info, tasks = handler(page)
                else:
                    info, tasks = None, None
            except Exception as e:
                task_q.put(task)
                continue
            if info:
                result_q.put((info, task))
                if tasks:
                    for task in tasks:
                        task_q.put(task)
            else:
                task_q.put(task)
            time.sleep(1)
    return worker
