from rosiok.items import RosiokItem
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider


class Rosiok(CrawlSpider):
    name = 'rosiok'

    allowed_domains = ['rosiok.com']

    start_urls = ['http://www.rosiok.com']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse,
                          errback=self.errback,
                          )

    def parse(self, response):
        yield self.parse_item(response)
        for a in response.css('a::attr(href)').extract():
            if 'rosiok' not in response.urljoin(a):
                continue
            yield Request(response.urljoin(a), callback=self.parse)

    def parse_item(self, response):
        il = ItemLoader(item=RosiokItem(), response=response)
        urls = response.css('img::attr(src)').extract()
        img = [url for url in urls if 'tu.68flash.com' in url]
        if img:
            il.add_value('image_urls', [url for url in urls if 'tu.68flash.com' in url])
            return il.load_item()

    def errback(self, response):
        pass
