import scrapy
from jiandan.items import JiandanItem
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider


class Jiandan(Spider):
    name = 'jiandan'
    start_urls = ['http://jandan.net/ooxx']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,
                                 errback=self.errback,
                                 )

    def parse(self, response):
        yield self.parse_item(response)
        next_page = response.xpath('//a[@class="previous-comment-page"]/@href').extract()
        if next_page:
            yield scrapy.Request(next_page[-1], callback=self.parse)

    def parse_item(self, response):

        il = ItemLoader(item=JiandanItem(), response=response)
        il.add_xpath('image_urls', '//a[@class="view_img_link"]/@href')
        return il.load_item()

    def errback(self, response):
        pass
