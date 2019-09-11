#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from carslogo.items import CarslogoItem
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider


class CarsLogo(CrawlSpider):
    name = 'cars'
    start_urls = ['http://www.pcauto.com.cn/zt/chebiao/']

    def parse(self, response):
        selector = Selector(response)
        carskind = selector.xpath('//div[@id="menu"]/ul/li/a/@href').extract()[1:]
        for each in carskind:
            yield Request(each, callback=self.parse_item)

    def parse_item(self, response):
        selector = Selector(response)
        item = CarslogoItem()
        item['country_name'] = selector.xpath('//div[@class="th"]/span[@class="mark"]/a/text()').extract()
        item['image_urls'] = selector.xpath('//div[@class="dPic"]/i[@class="iPic"]/a/img/@src').extract()
        item['car_names'] = selector.xpath('//div[@class="dPic"]/i[@class="iPic"]/a/img/@alt').extract()
        yield item
