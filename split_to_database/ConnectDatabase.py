# -*- coding: utf-8 -*-

"""
编写创建数据库的类，并构建connectMysql方法
author:王诚坤
date：2018/10/16
"""

import pymysql


class MySQLCommand(object):
    # 初始化类
    def __init__(self):
        # 数据库地址
        self.host = 'localhost'
        # 端口号
        self.port = 3306
        # 用户名
        self.user = 'root'
        # 密码
        self.password = 'root'
        # 数据库名
        self.db = 'scrapy'
        # 数据库表名
        self.table = 'completed'

    def connectMysql(self):
        """
        建立数据库连接
        :return:
        """
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except pymysql.Error as e:
            print('连接数据库失败！')
            print(e)

    def insertData(self, data_dict, primary_key='succorID'):
        '''
        将数据插入数据库，首先检查数据是否已经存在，如果存在则不插入
        :param data_dict: 要插入的数据字典
        :param primary_key: 主键
        :return:
        '''

        # 检测数据是否存在
        sqlExit = 'SELECT ' + primary_key + ' FROM completed WHERE ' + primary_key + " = %s " % (data_dict[primary_key])
        # 执行查找语句
        res = self.cursor.execute(sqlExit)
        if res:
            print('数据已经存入数据库', res)
            return 0
        # 数据不存在，则执行插入操作
        try:
            # 拼接属性名
            cols = ','.join(data_dict.keys())
            # 拼接属性名对应的值
            values = '","'.join(data_dict.values())
            # 插入语句
            sql = "INSERT INTO completed (%s) VALUES (%s)" % (cols, '"' + values + '"')

            try:
                # 执行插入操作
                result = self.cursor.execute(sql)
                insert_id = self.conn.insert_id()
                self.conn.commit()

                if result:
                    print('插入成功', insert_id)
                    return insert_id + 1
            except pymysql.Error as e:
                # 如果出现异常，执行回滚操作
                self.conn.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print('数据已存在，未再次插入！')
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因 %d: %s" % (e.args[0], e.args[1]))

    def closeMysql(self):
        """
        关闭数据库连接
        :return:
        """
        self.cursor.close()
        self.conn.close()
        print('数据库连接已关闭！')