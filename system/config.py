#coding=utf-8


def connect_db():
    import mysql.connector
    return mysql.connector.connect(user='root', password='', database='novel2love', use_unicode=True)
