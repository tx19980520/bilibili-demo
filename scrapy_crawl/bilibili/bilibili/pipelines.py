# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


#class BilibiliPipeline(object):
#    def process_item(self, item, spider):
#        return item

class bilibiliImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['animePictureUrl'];
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        item['animePicturePath'] = image_paths[0]
        return item
