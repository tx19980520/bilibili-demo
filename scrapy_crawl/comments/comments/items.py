# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentsItem(scrapy.Item):
    # define the fields for your item here like:
    animeId = scrapy.Field()
    comments = scrapy.Field()
    count = scrapy.Field()
    pass
