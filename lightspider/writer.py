import os
import json
import csv

from tqdm import tqdm

from lightutils import logger


def json_writer(result_q, task_nums, save_path):
    logger.info('写入地址为：{}， 临时文件地址为：{}'.format(save_path + os.sep + 'result.json',
                                              save_path + os.sep + 'handled.txt'))
    bar = tqdm(total=task_nums)
    while True:
        result, task = result_q.get(True)
        if result == '-end-':
            break
        with open(save_path + os.sep + 'result.json', 'a+', encoding='utf-8') as f:
            line = json.dumps(result, ensure_ascii=False)
            f.write(line + '\n')
        with open(save_path + os.sep + 'handled.txt', 'a+', encoding='utf-8') as f:
            f.write(task + '\n')
        bar.update()


def csv_writer(result_q, task_nums, save_path):
    logger.info('写入地址为：{}， 临时文件地址为：{}'.format(save_path + os.sep + 'result.csv',
                                              save_path + os.sep + 'handle.txt'))
    bar = tqdm(total=task_nums)
    while True:
        result, task = result_q.get(True)
        if result == '-end-':
            break
        with open(save_path + os.sep + 'result.csv', 'a+', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(result)
        with open(save_path + os.sep + 'handle.txt', 'a+', encoding='utf-8') as f:
            f.write(task + '\n')
        bar.update()
