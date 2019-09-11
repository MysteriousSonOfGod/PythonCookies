# coding=utf-8
import scrapy
from house.items import HouseItem
from house.scrapy_redis.spiders import RedisSpider
from scrapy.loader import ItemLoader


class Lianjia(RedisSpider):
    name = 'anjuke_item'
    redis_key = 'anjuke:start_urls'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        il = ItemLoader(item=HouseItem(), response=response)
        il.add_value('link', [response.url])
        il.add_value('code', [response.status])
        return il.load_item()
