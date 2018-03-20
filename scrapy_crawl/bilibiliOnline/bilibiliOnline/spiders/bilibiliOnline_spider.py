
# coding=utf-8
import time
import scrapy
import json
from items import BilibiliOnlineItem;
import re

class BilibiliSpider(scrapy.Spider):
    name = "bilibiliOnline"
    allowed_domains = ["bilibili.com"]
    start_urls=["https://www.bilibili.com"]
    def parse(self, response):
        sel=scrapy.Selector(response)
        select=response.xpath('//*[@id="home_popularize"]/div[2]/div[1]/a[1]')
        onlineWatch = re.search('在线观看：([\d]*)',select.extract()[0].encode('utf-8'))
        online = re.search('在线人数：([\d]*)',select.extract()[0].encode('utf-8'))
        select=response.xpath('//*[@id="home_popularize"]/div[2]/div[1]/a[2]')
        newVideo = re.search("最新投稿：([\d]*)",select.extract()[0].encode('utf-8'))
        item = BilibiliOnlineItem()
        item["online"] = online.group(1)
        item["onlineWatch"] = onlineWatch.group(1)
        item["newVideo"] = newVideo.group(1)
        item["time"] =time.time() 
        yield item;
