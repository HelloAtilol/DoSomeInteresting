# -*- coding: utf-8 -*-
"""
读取文件，只读取内容部分，并做简单分析。
author: 王诚坤
date: 2018/10/30
"""

from ConnectDatabase import MySQLCommand


def order_content(conn):
    last_time = 0
    title_list = ['createTime', 'content']
    result = conn.select_order(title_list)
    f = open('data/content.txt', 'w', encoding='utf-8')
    for res in result:
        if res[0] != last_time:
            f.write(res[1] + '\n')
            last_time = res[0]
    f.close()

def main():
    conn = MySQLCommand()
    conn.connectMysql()
    order_content(conn)
    conn.closeMysql()


if __name__ == '__main__':
    main()
