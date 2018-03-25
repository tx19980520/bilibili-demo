
import time
import os
import json
def jsonIn(file_dir):
    nowyear = time.localtime(time.time()-10*3600)[0]
    nowmonth = time.localtime(time.time()-10*3600)[1]
    nowdate = time.localtime(time.time()-10*3600)[2]
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
            if time.localtime(data['time'])[0] == nowyear and time.localtime(data['time'])[1] == nowmonth and time.localtime(data['time'])[2] == nowdate:
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
    intodb = False;
    hasinto = 0
    while True:
	if(time.localtime().tm_hour==23):
            hasinto = 1;
        cmd = "scrapy crawl bilibiliOnline -t json -o ./data/%s.json"%(str(int(time.time())))
        os.system(cmd)
        if(time.localtime().tm_hour==1 and hasinto == 0):
            intodb = True;
        time.sleep(200)
        if time.localtime().tm_hour==1 and intodb:
            file = jsonIn("data")
            cmd = "mongoimport --db bilibili --collection onlines --file /usr/share/nginx/html/bilibili-demo-back-end/scrapy_crawl/bilibiliOnline/bilibiliOnline/%s"%(file)
            os.system(cmd)
            intodb = False;
            hasinto = 1;


#main()
file = jsonIn("data")
cmd = "mongoimport --db bilibili --collection onlines --file /usr/share/nginx/html/bilibili-demo-back-end/scrapy_crawl/bilibiliOnline/bilibiliOnline/%s"%(file)
os.system(cmd)

