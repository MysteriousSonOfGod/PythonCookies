# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class MmtaobaoItem(Item):
    avatarUrl = Field()
    cardUrl = Field()
    city = Field()
    height = Field()
    weight = Field()
    realName = Field()
    totalFanNum = Field()
    totalFavorNum = Field()
    userId = Field()
