# -*- coding: utf-8 -*-

BOT_NAME = 'AiqiyiLaojiumen'
SPIDER_MODULES = ['AiqiyiLaojiumen.spiders']
NEWSPIDER_MODULE = 'AiqiyiLaojiumen.spiders'
ITEM_PIPELINES = {'AiqiyiLaojiumen.pipelines.LaojiumenPipelines': 1}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5(KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

COOKIES_ENABLED = False

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'WebSpider'
MONGODB_DOCNAME = 'laojiumen'

FEED_URI = 'laojiumen.csv'
FEED_FORMAT = 'csv'
