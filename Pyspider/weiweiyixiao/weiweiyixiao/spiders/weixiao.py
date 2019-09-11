#!/usr/bin/env python3

import json

from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from weiweiyixiao.items import WeiweiyixiaoItem


class WeixiaoQingcheng(CrawlSpider):
    name = 'qingcheng'

    url = 'http://comments.youku.com/comments/~ajax/vpcommentContent.html?__ap={"videoid":"424334763","showid":"300389","isAjax":1,"page":"%s"}'

    def start_requests(self):
        for num in range(1, 976 + 1):
            yield Request(self.url % num)

    def parse(self, response):
        item = WeiweiyixiaoItem()
        jsDict = json.loads(response.body.decode('utf-8'))
        comment = jsDict['con']['pageResult']['data']
        for each in comment:
            item['username'] = each['user']['userName']
            item['usercomment'] = each['text']
            yield item
