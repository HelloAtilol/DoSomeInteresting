# -*- coding: utf-8 -*-

import json
from ConnectDatabase import MySQLCommand

def splitTxt(filename, data_list, connection):
    """
    将文件分解并保存到数据库中，编码规则为utf-8，如果不匹配，可直接修改open中的encoding
    :param filename: 需要解析的文件名
    :param data_list: 需要保存到数据库中的字段
    :param connection: 建立的数据库连接
    :return:
    """
    # 统计标签
    count = 0
    errorcount = 0
    # 打开文件夹
    with open(filename, encoding='utf-8') as f:
        for text in f.readlines():
            result = {}

            # 此处try的是JSON的解析异常，如果仍然存在个别文件无法解析，将跳过，可以从console日志中查找,可以优化(TODO)
            # 如果出现大量无法插入的操作，则需要分析无法插入的文本出现的字符问题，修改文本初始化操作
            try:
                # 文本初始化操作
                # 将原文中url的双引号替换成##，如果要读取原来内容，只需要将##替换回来即可
                text = text.replace('\"', '##')
                # 将单引号换成双引号
                text = text.replace('\'', '\"')
                # 将None替换成""
                text = text.replace('None', "\"\"")
                # 将文本使用JSON解析

                # 将文本进行解析
                all_data = json.loads(text)
                # 建立需要插入数据库的字段
                for dl in data_list:
                    result[dl] = all_data[dl]
                # 如果是字典中嵌套字典，仍然需要手动编写，(TODO)
                result['needMoney'] = all_data['donate']['needMoney']
                result['recvedMoney'] = all_data['donate']['recvedMoney']
                # 调用方法插入数据
                connection.insertData(result)
                count += 1
            except json.decoder.JSONDecodeError as e:
                # 打印异常值
                print(text)
                errorcount += 1
                continue
    print('成功数量*****' + str(count))
    print('失败数量*****' + str((errorcount-count)/2))


if __name__ == '__main__':
    # 建立数据库连接
    conn = MySQLCommand()
    conn.connectMysql()
    # 将数据插入数据库
    # 要保存到数据库的字段
    data_list = ['succorID', 'title', 'cateName', 'cateTagName', 'summary', 'startTime', 'endTime']

    splitTxt('yijieshu.txt', data_list, conn)
    # 关闭数据库
    conn.closeMysql()
