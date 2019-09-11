import scrapy
from doubancomment.items import DoubancommentItem
from scrapy.loader import ItemLoader


class DoubanComment(scrapy.Spider):
    name = 'comment'

    start_urls = ['https://movie.豆瓣.com/subject/25921812/comments?sort=new_score&status=P']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,
                                 errback=self.errback)

    def parse(self, response):

        if response.status == 200:
            yield self.parse_item(response)
            next_page = response.xpath('//a[@class="next"]/@href').extract()[0]

            yield scrapy.Request('https://movie.豆瓣.com/subject/25921812/comments' + next_page, callback=self.parse)

    def parse_item(self, response):
        il = ItemLoader(item=DoubancommentItem(), response=response)
        il.add_xpath('comment', '//p[@class=""]/text()')
        il.add_xpath('title', '//span[contains(@class, "rating")]/@title')
        return il.load_item()

    def errback(self, response):
        pass
