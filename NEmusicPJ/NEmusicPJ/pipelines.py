# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class NemusicpjPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        self.db = self.client[settings['MONGODB_DBNAME']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
            # self.collection.insert(dict(item),{'writeConcern':{'w':1}})
            # print(self.db.getLastError())
        except:
            print('this item fail to insert!!')
            pass
        # self.collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
