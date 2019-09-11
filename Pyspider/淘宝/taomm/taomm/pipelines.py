# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class TaommPipeline(object):
    def process_item(self, item, spider):
        return item


class TaommImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['picUrl'], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = item['picId'] + '.jpg'
        filename = 'full/{0}/{1}/{2}'.format(item['city'], item['realName'], image_guid)
        return filename
