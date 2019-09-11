import json

from mmtaobao.items import MmtaobaoItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider


# 通过GooGLE-Chrome审查工具得到url="https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
# 接着ViewSource得到"q&viewFlag=A&sortType=default&searchStyle=&searchRegion=city%3A&searchFansNum=&currentPage=1&pageSize=100"
# 拼接url和ViewSource，删减不变必要的参数得到最终爬取的URL='https://mm.taobao.com/tstar/search/tstar_model.do?currentPage=1&pageSize=100'
# 经过测试页面总共411,日期10-5-2016
# mm相册主页可以简化为url = "https://mm.taobao.com/self/model_album.htm?user_id=%s"

class MmTaoBao(CrawlSpider):
    name = 'mm'

    # 仅仅需要翻页
    urlMM = 'https://mm.taobao.com/tstar/search/tstar_model.do?currentPage=%s&pageSize=100'

    # uesr_id和page
    # urlALBUM = 'https://mm.taobao.com/self/album/open_album_list.htm?user_id%20={0}&page=1'

    def start_requests(self):
        for num in range(1, 411 + 1):
            yield Request(self.urlMM % num)

    def parse(self, response):
        jsDict = json.loads(response.text)
        jsData = jsDict['data']['searchDOList']
        for each in jsData:
            item = MmtaobaoItem()
            item['avatarUrl'] = each['avatarUrl']
            item['cardUrl'] = each['cardUrl']
            item['city'] = each['city']
            item['height'] = each['height']
            item['weight'] = each['weight']
            item['realName'] = each['realName']
            item['totalFanNum'] = each['totalFanNum']
            item['totalFavorNum'] = each['totalFavorNum']
            item['userId'] = each['userId']
            yield item

            # yield Request(self.urlALBUM.format(each['userId']),callback=self.parse_page,meta={'userId':each['userId']})


"""
    def parse_page(self,response):
        selector = Selector(response)
        # userId = response.meta['userId']
        userId = '927018118'
        urlPage = 'https://mm.taobao.com/self/album/open_album_list.htm?user_id%20={0}&page={1}'
        totalPage = selector.xpath('//input[@name="totalPage"]/@value').extract()[0]
        # for i in range(1, int(totalPage) + 1):
        for i in range(1,2):
            yield Request(urlPage.format(userId,i),callback=self.parse_album)

    def parse_album(self,response):
        selector = Selector(response)
        href = selector.xpath('//p[@class="mm-fengmian clearfix"]/a[@class="mm-first"]/@href').extract()
        # for each in href:
        #     yield Request('https:' + each,callback=self.parse_image)
        yield Request('https:' + href[0], callback=self.parse_image)


    def parse_image(self,response):
        urlImage = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s&page=1'
        user_id = re.search('user_id=(\d.+)&album_id', response.url).group(1)
        album_id = re.search('album_id=(\d.+)&album_flag', response.url).group(1)
        yield Request(urlImage % (user_id,album_id),callback=self.parse_download,meta={'user_id':user_id,'album_id':album_id})


    def parse_download(self,response):
        print('caonimabi!!!!!!!!!!!!!\n\n\n\n\n\n')
        jsDict = json.loads(response.text)
        user_id = response.meta['user_id']
        album_id = response.meta['album_id']
        page = jsDict['totalPage']
        urlDownload = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s&page=%s'
        for i in range(1,int(page) + 1):
            yield Request(urlDownload % (user_id,album_id),callback=self.store_image)


    def store_image(self,response):
        print('I am here.............\n\n\n\n\n\n')
        jsDict = json.loads(response.text)
        jsData = jsDict['picList']
        for each in jsData:
            img = MmtaobaoImagesItem()
            img['picId'] = each['picId']
            temp = 'http:' + each['picUrl']
            img['picUrl'] = temp.split('.jpg_')[0] + '.jpg'
"""
