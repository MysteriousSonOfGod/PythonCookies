# -*- coding: utf-8 -*-

# Scrapy settings for weiweiyixiao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weiweiyixiao'

SPIDER_MODULES = ['weiweiyixiao.spiders']
NEWSPIDER_MODULE = 'weiweiyixiao.spiders'

ITEM_PIPELINES = {'weiweiyixiao.pipelines.WeiweiyixiaoPipeline': 1}

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'

COOKIES_ENABLED = False

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'WebSpider'
MONGODB_DOCNAME = 'weiweiyixiao'

FEED_URI = 'weiweiyixiao.csv'
FEED_FORMAT = 'csv'
