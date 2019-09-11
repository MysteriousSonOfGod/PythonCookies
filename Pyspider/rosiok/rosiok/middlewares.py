# coding:utf-8

from faker import Factory
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

fake = Factory.create()


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent):
        self.user_agent = fake.user_agent()
