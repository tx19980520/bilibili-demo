
import time
import os
import json
def jsonIn(file_dir):
    nowyear = time.localtime(time.time()-3*3600)[0]
    nowmonth = time.localtime(time.time()-3*3600)[1]
    nowdate = time.localtime(time.time()-3*3600)[2]
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
            print file
            f= open("./data/"+file,'r');
            try:
                data=json.loads(f.read())[0]
            except ValueError:
                f.close()
                os.remove("./data/"+file)
                continue
            if time.localtime(data['time'])[0] == nowyear and time.localtime(data['time'])[1] == nowmonth and time.localtime(data['time'])[2] == nowdate:
                point = {}
                y1 = int(data['online'])
                y2 = int(data['onlineWatch'])
                point['x'] = float(data['time'])*1000
                point['y1'] = y1/10000.0
                point['y2'] = y2/10000.0
                todayData['data'].append(point)
                os.remove("./data/"+file)
    dayfile.write(json.dumps(todayData))
    dayfile.close()
    return filename

def main():
    intodb = False;
    hasinto = 0
    while True:
	if(time.localtime().tm_hour==23):
            hasinto = 1;
        cmd = "scrapy crawl bilibiliOnline -t json -o ./data/%s.json"%(str(int(time.time())))
        os.system(cmd)
        if(time.localtime().tm_hour==1 and hasinto == 1):
            intodb = True;
        time.sleep(100)
        if intodb:
            modifyFile = jsonIn("./data")
            cmd = "mongoimport --db bilibili --collection onlines --file /usr/share/nginx/html/bilibili-demo-back-end/bilibili-demo-back-end/scrapy_crawl/bilibiliOnline/bilibiliOnline/%s"%(modifyFile)
            os.system(cmd)
             
            intodb = False;
            hasinto = 0;


main()
#filename = jsonIn("D:/Web_Objects/practice/react-redux-express/back-end/scrapy_crawl/bilibiliOnline/bilibiliOnline/data")
#cmd = "mongoimport --db bilibili --collection onlines --file D:\\Web_Objects\\practice\\react-redux-express\\back-end\\scrapy_crawl\\bilibiliOnline\\bilibiliOnline\\%s"%(#filename)
