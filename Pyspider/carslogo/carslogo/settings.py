# -*- coding: utf-8 -*-

# Scrapy settings for carslogo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'carslogo'

SPIDER_MODULES = ['carslogo.spiders']
NEWSPIDER_MODULE = 'carslogo.spiders'

ITEM_PIPELINES = {'carslogo.pipelines.CarsImagesPipeline': 2,
                  'carslogo.pipelines.CarslogoPipeline': 1}

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

IMAGES_STORE = '.'
