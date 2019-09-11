# coding=utf-8

import redis
import scrapy
from house.scrapy_redis.spiders import RedisSpider


class Lianjia(RedisSpider):
    name = 'anjuke_links'
    redis_key = 'anjuke:anjuke_urls'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="zu-info"]/h3/a/@href').extract()
        r = redis.StrictRedis()
        if urls:
            for url in urls:
                r.lpush('anjuke:start_urls', url)
        next_page = response.xpath('//a[@class="aNxt"]/@href').extract()
        if next_page:
            r.lpush('anjuke:anjuke_urls', next_page[0])
