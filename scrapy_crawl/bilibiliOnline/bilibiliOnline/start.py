import time
import os
import json
def jsonIn(file_dir):
    nowyear = time.localtime(time.time())[0]
    nowmonth = time.localtime(time.time())[1]
    nowdate = time.localtime(time.time())[2]
    todayData = {}
    todayData['year'] = nowyear
    todayData['month'] = nowmonth
    todayData['date'] = nowdate
    todayData['data'] = []
    filename = "modifyData/%s.json"%(str(nowyear)+str(nowmonth)+str(nowdate))
    dayfile = open(filename,"w")
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if(file == "image.py"):
                continue;
            f= open("data/"+file,'r');
            data=json.loads(f.read())[0]
            if time.localtime(data['time'])[0] == nowyear and time.localtime(data['time'])[1] == nowmonth and time.localtime(data['time'])[2] == 15:
                point = {}
                y1 = int(data['online'])
                y2 = int(data['onlineWatch'])
                point['x'] = float(data['time'])*1000
                point['y1'] = y1/10000.0
                point['y2'] = y2/10000.0
                todayData['data'].append(point)
    dayfile.write(json.dumps(todayData))
    return filename

def main():
    while True:
        cmd = "scrapy crawl bilibiliOnline -t json -o ./data/%s.json"%(str(int(time.time())))
        if(time.localtime().tm_hour>=6 and time.localtime().tm_hour<=23):
            os.system(cmd)
            time.sleep(300)
        else:#这个地方我们的准备进行一次数据输入数据库
            jsonIn("D:/Web_Objects/practice/react-redux-express/back-end/scrapy_crawl/bilibiliOnline/bilibiliOnline/data")
            time.sleep(60*6)


filename = jsonIn("D:/Web_Objects/practice/react-redux-express/back-end/scrapy_crawl/bilibiliOnline/bilibiliOnline/data")
cmd = "mongoimport --db bilibili --collection onlines --file D:\\Web_Objects\\practice\\react-redux-express\\back-end\\scrapy_crawl\\bilibiliOnline\\bilibiliOnline\\%s"%(filename)
os.system(cmd)
