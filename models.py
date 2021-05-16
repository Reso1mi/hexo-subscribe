import time
from peewee import *
import config

import mysql.connector

mysql_db = MySQLDatabase("subscribe", host=config.DATABASE_CONFIG['host'], user=config.DATABASE_CONFIG['user'],
                         passwd=config.DATABASE_CONFIG['passwd'],
                         charset="utf8")
mysql_db.connect()  # 连接数据库


class MySQLModel(Model):
    class Meta:
        database = mysql_db


class Addr(MySQLModel):  # 类的小写即表名
    ID = AutoField()  # 字段声明，自动递增主键
    name = CharField()
    email = CharField()
    ip = CharField()
    create_date = DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# 建表
Addr.create_table()
