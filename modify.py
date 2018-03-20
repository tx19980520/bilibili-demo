import json

f = open('bilibili.json','r');
data = json.loads(f.read())
for item in data:
    item['__v'] =0
    item['animePicturePath'] = item['animePicturePath'][0]
f.close();
f =open('bilibili.json','w');
f.write(json.dumps(data))
f.close()
