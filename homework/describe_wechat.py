# -*- coding: utf-8 -*-
"""
1. 将聊天数据按照群号，划分不同的文件 √
2. 统计每个群中发言次数最多的ID
3. 统计每个群的活跃度，和所有群加起来的活跃度，在每天时间上的分布
4. 统计每个人的发言长短，和平均长度；
5. 统计每个群中，被@的次数
6. 统计四个群中被@的次数
7. 统计用户发链接或图片的次数(也可以统计发图片链接的次数/总发言数)
8. 四个群分别提到最多的词(去掉stopwords)
"""

from ConnectDatabase import MySQLCommand
import time
import os
import re


def getChatRoom(connector):
    """
    数据库返回的数据：第7列为时间（时间为timestamp毫秒类型，需要除以1000取整），第8列为群号，第9列为具体ID和聊天内容
    :param connector: 数据库缓冲池
    :return:
    """
    sql = "select * from wechat_message "
    result = connector.execute(sql)
    for t in range(result):
        print('第', t + 1, '条内容正在划分~')
        one_message = connector.fetchone()
        room_num = one_message[7]
        with open('data/' + room_num + '.txt', 'a', encoding='utf-8') as f:
            f.write(deal_time(one_message[6]) + '\t' + one_message[8] + '\n')
    print('******文件划分完成(没有遇到BUG)!!!******')


def countSender(connector):
    file_list = os.listdir('data/')

    # 将内容分解的正则表达式
    re_con = re.compile(r'^(.*)(:\n)(.*)')

    sql = "select content from wechat_message where talker = "
    for file_name in file_list:
        file_name = file_name.replace('.txt', '')
        final_sql = sql + "'" + file_name + "'"
        res = connector.execute(final_sql)
        for t in range(5):
            context = connector.fetchone()[0]
            # print(context)
            split_res = re_con.match(context)
            # 获取用户ID
            user_id = split_res[1]


def deal_time(times):
    """
    将时间戳timestamp转换为北京时间
    :param times:
    :return:
    """
    t = time.localtime(int(times / 1000))
    return time.strftime('%Y-%m-%d %H:%M:%S', t)


def main():
    # 建立数据库连接
    conn = MySQLCommand()
    conn.connectMysql()
    """
    # 1. 将聊天数据按照群号，划分不同的文件 
    getChatRoom(conn.cursor)
    """
    countSender(conn.cursor)
    # 关闭数据库连接
    conn.closeMysql()


if __name__ == '__main__':
    main()
