# -*- coding: utf-8 -*-
# @Time    : 2020/5/23 20:56
# @Author  : lightsmile
# @Software: PyCharm

from lightspider.baike import table

if __name__ == '__main__':
    word = "曹操"
    print(table.query(word))
    for item in table.query(word):
        print(table.get_table(item[1]))

