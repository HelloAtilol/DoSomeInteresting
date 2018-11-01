# -*- coding: utf-8 -*-
"""
读取文件，只读取内容部分，并做简单分析。
author: 王诚坤
date: 2018/10/30
"""

from ConnectDatabase import MySQLCommand
import re

def order_content(conn):
    last_sid = ''
    title_list = ['createTime', 'msgSvrId', 'content']
    result = conn.select_order(title_list)
    at_dict = {}
    f = open('data/content.txt', 'w', encoding='utf-8')
    for res in result:
        # 去除重复
        if res[1] != last_sid:
            content = res[2]
            only_content, only_at = get_id_content(content)
            f.write(only_content + '\n')
            last_sid = res[1]
    f.close()
    return at_dict

def get_id_content(content):
    re_con = re.compile(r'^(.*)(:\n)(.*)')
    re_at = re.compile(r'^(.*?)(@)(.*)([\?\s]+)')
    id_content = re_con.match(content)
    only_at = ''
    try:
        only_content = content.replace(id_content.group(1)+id_content.group(2), '')
        if '<' in only_content:
            return only_content, ''
        at_content = re_at.match(only_content)
        if at_content is not None:
            only_at = at_content.group(2)
            only_content = only_content.replace(at_content.group(0), '')
    except AttributeError:
        only_content = ''
    return only_content, only_at


def main():
    conn = MySQLCommand()
    conn.connectMysql()
    order_content(conn)
    conn.closeMysql()


if __name__ == '__main__':
    main()
