# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #__v = scrapy.Field()
    uid = scrapy.Field()
    vip = scrapy.Field()#关于后续的使用vip对学习的支持
    likevideo = scrapy.Field()
