
# coding=utf-8
import time
import scrapy
import json
#from items import TestItem;
from items import BilibiliOnlineItem;
import re

class BilibiliSpider(scrapy.Spider):
    name = "bilibiliOnline"
    allowed_domains = ["bilibili.com"]
    start_urls=["https://www.bilibili.com"]
    def parse(self, response):
        sel=scrapy.Selector(response)
        select=response.xpath('//*[@id="home_popularize"]/div[2]/div[1]/a[1]')
        online = re.search('([\d]+)[^0-9]+([\d]+)',select.extract()[0].encode('utf-8'))
        select=response.xpath('//*[@id="home_popularize"]/div[2]/div[1]/a[2]')
        newVideo = re.search("([\d]+)",select.extract()[0].encode('utf-8'))
        item = BilibiliOnlineItem()
        #item = TestItem()
        if online is not None:
            item["online"] = online.group(1)
        if online is not None:
            item["onlineWatch"] = online.group(2)
        if newVideo is not None:
            item["newVideo"] = newVideo.group(1)
        item["time"] =time.time()
       #item['total'] = onlineWatch.group(1);
        yield item;
