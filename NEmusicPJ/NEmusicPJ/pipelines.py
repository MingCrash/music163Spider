# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class NemusicpjPipeline(object):
    def __init__(self):
        client=pymongo.MongoClient(host=settings['MONGODB_HOST'],port=settings['MONGODB_PORT'])
        db=client[settings['MONGODB_DBNAME']]
        self.collection=db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        try:
            if self.collection.insert(dict(item)):
                print('successful!!')
        except:
            pass
        return item
