import json
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from taomm.items import TaommItem


class Taomm(CrawlSpider):
    name = 'taomm'

    # def start_requests(self):
    #     url = 'https://mm.taobao.com/self/album/open_album_list.htm?user_id%20=777105914&page=1'
    #     yield Request(url,meta={'realName':'wobugaosunia','city':'shabibibi'})

    def start_requests(self):
        url = 'https://mm.taobao.com/self/album/open_album_list.htm?user_id%20={0}&page=1'
        with open('mm.json', 'r') as f:
            jsDict = json.loads(f.read())

        for each in jsDict:
            yield Request(url.format(each['userId']), meta={'realName': each['realName'], 'city': each['city']})

    # 获取总的页数
    def parse(self, response):
        selector = Selector(response)
        realName = response.meta['realName']
        city = response.meta['city']
        userId = re.search('user_id%20=(\d+)&page', response.url).group(1)
        urlPage = 'https://mm.taobao.com/self/album/open_album_list.htm?user_id%20={0}&page={1}'
        totalPage = selector.xpath('//input[@name="totalPage"]/@value').extract()[0]
        for i in range(1, int(totalPage) + 1):
            yield Request(urlPage.format(userId, i), callback=self.parse_page,
                          meta={'realName': realName, 'city': city})

    # 获取每个页面的相册
    def parse_page(self, response):
        selector = Selector(response)
        realName = response.meta['realName']
        city = response.meta['city']
        href = selector.xpath('//p[@class="mm-fengmian clearfix"]/a[@class="mm-first"]/@href').extract()
        for each in href:
            yield Request('https:' + each, callback=self.parse_album,
                          meta={'realName': realName, 'city': city})  # 返回每一个相册页面

    # 获取相册的总页数

    def parse_album(self, response):
        realName = response.meta['realName']
        city = response.meta['city']
        urlAlbum = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s&page=1'
        user_id = re.search('user_id=(\d+)&album_id', response.url).group(1)
        album_id = re.search('album_id=(\d+)&album_flag', response.url).group(1)
        yield Request(urlAlbum % (user_id, album_id), callback=self.parse_image,
                      meta={'realName': realName, 'city': city})

    def parse_image(self, response):
        realName = response.meta['realName']
        city = response.meta['city']
        jsDict = json.loads(response.text)
        page = jsDict['totalPage']
        user_id = re.search('user_id=(\d+)&album_id', response.url).group(1)
        album_id = re.search('album_id=(\d+)&page', response.url).group(1)
        urlImage = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s&page=%s'
        for i in range(1, int(page) + 1):
            yield Request(urlImage % (user_id, album_id, i), callback=self.image,
                          meta={'realName': realName, 'city': city})

    def image(self, response):
        realName = response.meta['realName']
        city = response.meta['city']
        jsDict = json.loads(response.text)
        picList = jsDict['picList']
        for img in picList:
            item = TaommItem()
            item['realName'] = realName
            item['city'] = city
            item['picId'] = img['picId']
            temp = 'http:' + img['picUrl']
            item['picUrl'] = temp.split('.jpg_')[0] + '.jpg'
            yield item
