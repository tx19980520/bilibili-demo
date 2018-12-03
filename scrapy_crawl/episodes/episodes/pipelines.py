# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import spiders.items as Items
from scrapy.exporters import JsonLinesItemExporter
fileBilibili = open("./data/episodes.json",'w')
exporterBilibili = JsonLinesItemExporter(fileBilibili,encoding="utf-8",ensure_ascii=False)
exporterBilibili.start_exporting()
class EpisodesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['url']
        for url in image_url:
            yield scrapy.Request(url)
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        for path in image_paths:
            item["coverpath"].append("/full/episodes/"+path[5:])
        exporterBilibili.export_item(item)
    def close_spider(self,spider):
        exporterBilibili.finish_exporting()
        fileBilibili.close()
