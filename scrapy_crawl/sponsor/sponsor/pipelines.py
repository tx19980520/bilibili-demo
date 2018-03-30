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
from scrapy.exceptions import CloseSpider
class SponsorPipeline(object):
    def __init__(self):
        self.fuck=False
        self.sponsorFile = open("./data/sponsortest.json","wb")
        self.exporter = JsonLinesItemExporter(self.sponsorFile,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()
        self.uset = set();
    def process_item(self, item, spider):
        if item['uid'] in self.uset:
            raise DropItem("User has been add in the collection.")
        else:
            self.uset.add(item['uid'])
            self.exporter.export_item(item);
            return item;
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.sponsorFile.close()
