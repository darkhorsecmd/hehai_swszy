# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import scrapy
from scrapy.exceptions import DropItem
import MySQLdb
import MySQLdb.cursors


class HehaiSwszyPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 这个方法会在初始化的时候被scrapy调用
        db_params = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool("MySQLdb", **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted 将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        if item["birth_date"] is not None:
            # 有birth_date
            insert_sql = '''
                insert into swszy(url_object_id,url,image_url,name,sex,nation,birth_date,politics,education,degree,position,address,phone,email,description)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            cursor.execute(insert_sql,
                           (
                               item["url_object_id"], item["url"], item["image_url"], item["name"], item["sex"],
                               item["nation"],
                               item["birth_date"], item["politics"], item["education"], item["degree"],
                               item["position"], item["address"], item["phone"], item["email"], item["description"]))
        else:
            insert_sql = '''
                 insert into swszy(url_object_id,url,image_url,name,sex,nation,politics,education,degree,position,address,phone,email,description)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
            cursor.execute(insert_sql,
                           (
                               item["url_object_id"], item["url"], item["image_url"], item["name"], item["sex"],
                               item["nation"],
                               item["politics"], item["education"], item["degree"],
                               item["position"], item["address"], item["phone"], item["email"], item["description"]))
