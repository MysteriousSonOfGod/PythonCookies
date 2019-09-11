# -*- coding: utf-8 -*-

from datetime import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class HousePipeline(object):
    def __init__(self, mongodb_host, mongodb_port, mongodb_dbname, mongodb_docname):
        # self.mongodb_host = mongodb_host
        # self.mongodb_port = mongodb_port
        # self.mongodb_dbname = mongodb_dbname
        self.client = pymongo.MongoClient(host=mongodb_host, port=mongodb_port)
        self.tdb = self.client[mongodb_dbname]
        self.post = self.tdb[mongodb_docname]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_host=crawler.settings.get('MONGODB_HOST'),
            mongodb_port=crawler.settings.get('MONGODB_PORT'),
            mongodb_dbname=crawler.settings.get('MONGODB_DBNAME'),
            mongodb_docname=crawler.settings.get('MONGODB_DOCNAME')
        )

    def open_spider(self, spider):
        with open('time', 'a') as f:
            f.write(str(datetime.now()))

    def close_spider(self, spider):
        with open('time', 'a') as f:
            f.write(str(datetime.now()))

    def process_item(self, item, spider):
        print(dict(item))
        self.post.insert(dict(item))
        return item
