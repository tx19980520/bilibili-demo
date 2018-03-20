# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliOnlineItem(scrapy.Item):
    # define the fields for your item here like:
    onlineWatch = scrapy.Field()
    online = scrapy.Field()
    newVideo = scrapy.Field()
    time = scrapy.Field()
