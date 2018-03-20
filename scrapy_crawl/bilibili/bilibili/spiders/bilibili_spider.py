# coding=utf-8
import scrapy
import json
from items import BilibiliItem;

start_urls = []
for page in range(1,152):
    url = "https://bangumi.bilibili.com/web_api/season/index_global?page=%d&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0"%(page)
    start_urls.append(url)
class BilibiliSpider(scrapy.Spider):
    name = "bilibili"
    allowed_domains = ["bilibili.com"]
    start_urls=start_urls
    def parse(self, response):
        body= json.loads(response.body)
        result =body['result']
        animeList = result['list']
        for anime in animeList:
            item = BilibiliItem()
            item["animeId"] = anime['season_id']
            item["animeTitle"] = anime["title"]
            item["animePictureUrl"] = anime["cover"]
            item['fans'] = anime['favorites']
	    item['animeFinished'] = anime['is_finish']
            yield item;
