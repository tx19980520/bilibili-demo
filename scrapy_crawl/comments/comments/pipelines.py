# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import json

class CommentsPipeline(object):
    def __init__(self):
        self.fileSpecific = open('./data/comments.json','ab')
        self.exporterSpecific = JsonLinesItemExporter(self.fileSpecific,encoding="utf-8",ensure_ascii=False)
        self.exporterSpecific.start_exporting()
    def process_item(self,item,spider):
        self.exporterSpecific.export_item(item)

    def close_spider(self,spider):
        self.exporterSpecific.finish_exporting()
        self.fileSpecific.close()
