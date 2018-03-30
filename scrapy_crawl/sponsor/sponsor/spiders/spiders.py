# -*- coding: utf-8 -*-
import scrapy
import json
import time
from pymongo import MongoClient
import items as Item
class BilibiliSponsorSpider(scrapy.Spider):
    name="sponsor"
    allowed_domains=['bilibili.com']
    def __init__(self):
        super(scrapy.Spider,self).__init__();
        client = MongoClient('mongodb://ty0207:1234512345qwe@106.15.225.249:27017/bilibili')
        db = client.bilibili
        collection = db.animes
        res = collection.find({},{"animeId":1})
        self.animeIds=[]
        for item in res:
             self.animeIds.append(item['animeId']);
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
        self.secondheaders={
    "Accept": "*/*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Connection": "keep-alive",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"Cookie": "fts=1507175456; sid=d8ragyld; UM_distinctid=15eefea7769125-0c8c038fcf3c3a-464a0129-e1000-15eefea776ae2; pgv_pvi=7160499200; biliMzIsnew=1; biliMzTs=null; rpdid=llplmlqoqdoswmiqwsiw; buvid3=B7EBA057-54AC-4687-AEBA-77629AE6232316840infoc; LIVE_BUVID=deb1b7d8cbfc0790c1e13ac4f8f1c974; LIVE_BUVID__ckMd5=14223e1b07238876; im_seqno_13567133=1997; LIVE_PLAYER_TYPE=2; _cnt_dyn=0; uTZ=-480; finger=edc6ecda; DedeUserID=13567133; DedeUserID__ckMd5=1c7cec4ddca7680f; SESSDATA=5d10c274%2C1524279600%2Cc697f7e3; bili_jct=09bb994401fb79745061fbc36fb73e46; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1522280743; _dfcaptcha=9734cdbb9b2de54a1d91382bacf730b1; CNZZDATA2724999=cnzz_eid%3D1304789830-1507347720-http%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1522410663",
"Host": "space.bilibili.com",
"Origin": "https://space.bilibili.com",
"Referer": "https://space.bilibili.com/17212494",
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"
    }
        self.get_user_url = "https://space.bilibili.com/ajax/member/GetInfo"
        self.common_url="https://bangumi.bilibili.com/sponsor/rankweb/get_sponsor_total"
    def start_requests(self):#这个地方把所有的投喂榜拿出来
        for id in self.animeIds:
            review  = "https://bangumi.bilibili.com/review/web_api/long/list?media_id=%s&folded=0&page_size=20&sort=0"%(id)
            nowbody = "season_id=%s&page=1&pagesize=100&csrf=09bb994401fb79745061fbc36fb73e46"%(id)
            yield scrapy.Request(self.common_url,method="POST",headers=self.headers,body=nowbody,meta={"id":id},callback=self.parse)
            yield scrapy.Request(review,method="GET",callback=self.review_parse)

    def review_parse(self,response):#for the user list
        print "review_parse"
        body = json.loads(response.body)
        if True:
            result = body['result'];
            #for review in result['list']:
            #uid = review['author']['mid']
            reviewbody = "mid=17212494&csrf=09bb994401fb79745061fbc36fb73e46"#"mid=%d&csrf=09bb994401fb79745061fbc36fb73e46"%(uid)
            yield scrapy.Request(self.get_user_url,method="POST",meta={"id":"17212494"},headers=self.secondheaders,body=reviewbody,callback=self.get_user)
                #next = "https://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=1"%(uid)
                #yield scrapy.Request(next,meta={"id":uid},callback=self.review_getuser)
    def get_user(self,response):
        print "get_user"
        body = json.loads(response.body)
        if True:
            data = body['data']
            item = Item.BilibiliUserItem()
            item['uid']= data['mid']#发现这个是字符串的
            item['vip'] = data['vip']
            item['likevideo'] = []
            next = "https://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=1"%(data['mid'])
            yield scrapy.Request(next,meta={"item":item},callback=self.user_detail)
    def parse(self,response):
        result = json.loads(response.body)['result']
        userList = result['list']
        for user in userList:
            item = Item.BilibiliUserItem()
            #item['__v'] = 0
            item['uid'] = user['uid']
            item['vip'] = user['vip']
            item['likevideo'] = []
            next = "https://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=1"%(user['uid'])
            yield scrapy.Request(next,meta={"item":item},callback=self.user_detail)
    def user_detail(self,response):
        print "user_detail"
        body = json.loads(response.body)
        status = body['status']
        if(status):
            data = body['data']
            for anime in data['result']:
                response.meta['item']['likevideo'].append(anime['season_id'])
            if(int(data['pages']) == 1):
                yield response.meta['item']
            else:
                for i in range(2,int(data['pages'])+1):
                    next = "https://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=%d"%(response.meta['item']['uid'],i)
                    yield scrapy.Request(next,callback=self.anime_detail,meta={"item":response.meta['item'],"page":i})#这个地方把某个具体的人的追番拿来继续分页得到
                    #time.sleep(0.05)
    def anime_detail(self,response):
        anime=json.loads(response.body)
        data = anime['data']
        for anime in data['result']:
            response.meta['item']['likevideo'].append(anime['season_id'])
        if response.meta['page'] == int(data['pages']):
            yield response.meta['item']
