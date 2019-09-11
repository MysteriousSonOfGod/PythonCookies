# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline


class CarslogoPipeline(object):
    def process_item(self, item, spideir):
        return item


class CarsImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item, 'index': item['image_urls'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        index = request.meta['index']
        image_guid = item['car_names'][index] + '.' + request.url.split('.')[-1]
        filename = 'full/{0}/{1}'.format(item['country_name'][0], image_guid)
        return filename
