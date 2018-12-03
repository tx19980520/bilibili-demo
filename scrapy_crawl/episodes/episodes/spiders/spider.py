import time
import json
import scrapy
start_urls = []
class EpisodesItem(scrapy.Item):
    url = scrapy.Field()
    coverpath = scrapy.Field()
    animeId = scrapy.Field()
    url = scrapy.Field()
'''
for bilibili specific and bilibili simple data;
'''
all = open("./specific_final.json")
for line in all.readlines():
    data = json.loads(line)
    url="http://bilibili.cqdulux.cn/api/AnimeSpecific/%d"%(data["animeId"])
    start_urls.append(url)
class EpisodesSpider(scrapy.Spider):
    name = "episodes"
    allowed_domains = ["bilibili.cqdulux.cn","bilibili.com"]
    start_urls=start_urls
    def parse(self, response):
        body = json.loads(response.body)
        result = body
        item = EpisodesItem()
        item["url"] = []
        item["coverpath"] = []
        item["animeId"] = result["specific"]["animeId"]
        for e in result["specific"]["episodes"]:
            item["url"].append(e["cover"])
        yield item
        
