import asyncio
from asyncio import Queue

from aiohttp import ClientSession
from faker import Factory
from lxml import etree

fake = Factory.create()


class Douban(object):
    def __init__(self, max_tries=2, account='603269622@qq.com', password='742369wo'):
        self.account = account
        self.password = password
        self.max_tries = max_tries
        self._session = None
        self.seen_urls = set()
        self.q = Queue()

    @property
    def session(self):
        if self._session is None:
            self._session = ClientSession(
                headers={'User-Agent': fake.user_agent()})
        return self._session

    async def login(self):
        url = 'https://accounts.豆瓣.com/login'
        response = await self.session.get(url, headers={'User-Agent': fake.user_agent()})
        rs = await response.text()

        data = {'source': 'None',
                'redir': 'https://www.豆瓣.com',
                'form_email': self.account,
                'form_password': self.password,
                'remember': 'on',
                'login': '登录'
                }
        sel = etree.HTML(rs)
        if 'name="ck"' in rs:
            data['ck'] = sel.xpath('//input[@name="ck"]/@value')[0]

        captcha_image = sel.xpath('//img[@id="captcha_image"]/@src')
        if captcha_image:
            captcha_image = captcha_image[0]
            captcha_id = sel.xpath('//input[@name="captcha-id"]/@value')[0]
            captcha_solution = input('请手动输入验证码，网址为' + captcha_image + '\n')
            data['captcha-solution'] = captcha_solution
            data['captcha-id'] = captcha_id
        await self.session.post(url, data=data, headers={'User-Agent': fake.user_agent()})
        self._session = self.session

    async def fetch(self, url='https://www.豆瓣.com/people/121124248/', sign='first'):
        url = 'https://www.豆瓣.com/people/121124248/'
        await self.login()
        response = await self._session.get(url)
        text = await response.read()
        print(text.decode())


if __name__ == '__main__':
    douban = Douban()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(douban.fetch())
    loop.close()
