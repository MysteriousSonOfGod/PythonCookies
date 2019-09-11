# scrapy的坑

根目录为**scrapy.cfg**所在目录

单个函数只有一个返回值 **不要用** yield item，因为不会传输到轨道里，要用return item

倘若git clone 里包含.pyc，要把它删除，要不然程序不能运行，由于版本的原因

scrapy相关小提示

-o xx(保存数据的文件)
 -t xx(声明文件的后缀)


-s LOG_FILE=xx.log(将日记保存)，此时日志也不输出


--nolog(不输出日志)

-s JOBDIR=xx(保存采集列表)通过ctrl+c停止，然后再次运行命令'scrapy crawl xx -s JOBDIR=xx’

shell技巧
scrapy shell -s USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36' 'URL'

或者 scrapy shell
url = ''
request = scrapy.Request(url, headers={'User-Agent':''})
fetch(request)

settings里面为ITEM_PIPELINES，不是ITEM_PIPELINE,还有记得开启PIPELINES

headers设置
scrapy shell -s USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36' URL
settings里面为ITEM_PIPELINES，不是ITEM_PIPELINE,还有记得开启PIPELINES

CONCURRENT_REQUESTS = 100 注释
COOKIES_ENABLED = False 注释
ROBOTSTXT_OBEY = False 注释


LOG_LEVEL = 'INFO'

RETRY_ENABLED = False

REDIRECT_ENABLED = False

DOWNLOAD_TIMEOUT = 15

在settings里设置如下:
myproject为项目名称

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'myproject.middlewares.RotateUserAgentMiddleware': 400,
}

记住IMAGES_STORE = '.'
网页要加http
或者在pipelines.py里设置
from scrapy import signals
from datetime import datetime

class ShanchuPipeline(object):

    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        with open('时间.txt','a+') as f:
            f.write('开启爬虫的时间:-->'+str(datetime.now())+'\n')

    def spider_closed(self, spider):
        with open('时间.txt','a+') as f:
            f.write('结束爬虫的时间:-->'+str(datetime.now())+'\n')

    def process_item(self, item, spider):
        return item
