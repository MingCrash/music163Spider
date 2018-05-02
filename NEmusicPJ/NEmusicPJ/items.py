# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    singer=scrapy.Field()
    song=scrapy.Field()
    nickname=scrapy.Field()
    comment_content=scrapy.Field()
    likedCount=scrapy.Field()
    time=scrapy.Field()

class SingerItem(scrapy.Item):
    _id=scrapy.Field()
    singername=scrapy.Field()
    # singerheadimg=scrapy.Field()
    singerurl=scrapy.Field()

# class Albuminfo(scrapy.Item):
#     albumid=scrapy.Field()
#     albumintro=scrapy.Field()



