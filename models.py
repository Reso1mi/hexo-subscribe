import time
from peewee import *

# 改为SQLite3
sqlite_db = SqliteDatabase('./address.db')


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Addr(BaseModel):  # 类的小写即表名
    id = PrimaryKeyField()  # 字段声明，自动递增主键
    name = TextField()
    email = TextField()
    ip = TextField()
    create_date = DateTimeField(default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


Addr.create_table()
