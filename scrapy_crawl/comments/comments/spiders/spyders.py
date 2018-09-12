# -*- coding: utf-8 -*-
import scrapy
import json
import time
class CommentsItem(scrapy.Item):
    # define the fields for your item here like:
    animeId = scrapy.Field()
    comments = scrapy.Field()
    count = scrapy.Field()
    pass
class AlluserSpider(scrapy.Spider):
    name="comments"
    allowed_domains=['bilibili.com']
    def __init__(self):
        self.headers={
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"fts=1507175456; sid=d8ragyld; UM_distinctid=15eefea7769125-0c8c038fcf3c3a-464a0129-e1000-15eefea776ae2; pgv_pvi=7160499200; biliMzIsnew=1; biliMzTs=null; rpdid=llplmlqoqdoswmiqwsiw; buvid3=B7EBA057-54AC-4687-AEBA-77629AE6232316840infoc; LIVE_BUVID=deb1b7d8cbfc0790c1e13ac4f8f1c974; LIVE_BUVID__ckMd5=14223e1b07238876; im_seqno_13567133=1997; LIVE_PLAYER_TYPE=2; _cnt_dyn=0; uTZ=-480; finger=edc6ecda; DedeUserID=13567133; DedeUserID__ckMd5=1c7cec4ddca7680f; SESSDATA=5d10c274%2C1524279600%2Cc697f7e3; bili_jct=09bb994401fb79745061fbc36fb73e46; _dfcaptcha=e57e10b8fdbea52ff4f6d5ee069c951d",
    "Host":"bangumi.bilibili.com",
    "Origin":"https://bangumi.bilibili.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
    }
        self.common_url = "https://bangumi.bilibili.com/review/web_api/long/list"
        super(scrapy.Spider,self).__init__()
        self.animesId = []
        with open("D:\\js_web\\bilibili-demo-back-end\scrapy_crawl\\bilibili\\bilibili\\data\\bilibili.json",'r', encoding='UTF-8') as f:
            count = 1
            for line in f:
                # print(count)
                # count += 1 
                anime = json.loads(line)
                self.animesId.append(anime["animeId"]) 
    def start_requests(self):#这个地方把所有的投喂榜拿出来
        for anime in self.animesId:
            url = "?media_id=%s&folded=0&page_size=20&sort=0"%(anime)
            url = self.common_url + url
            yield scrapy.Request(url,method="GET",meta={"id":anime},headers=self.headers)
    def parse(self,response):
        if response.status == 200:
            result = json.loads(response.body)['result']
            if(isinstance(result,dict)):
                item = CommentsItem()
                item['animeId'] = response.meta["id"]
                item["comments"] = result["list"]
                item['count'] = result["total"]
                yield item