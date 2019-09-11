# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Laojiumen(Item):
    commentName = Field()
    commentTitle = Field()
    commentView = Field()
    commentScore = Field()
