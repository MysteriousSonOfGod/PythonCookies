import asyncio
from asyncio import Queue
from datetime import datetime

import aiofiles
import aiohttp
from faker import Factory
from lxml import etree

fake = Factory.create()


class Crawler(object):
    def __init__(self, max_redirect=10, max_tries=4,
                 max_tasks=10, loop=asyncio.get_event_loop()):
        self.loop = loop
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        self.time_start = datetime.now()
        self.time_end = None
        self._session = None

    @property
    def session(self):
        headers = {'User-Agent': fake.user_agent()}
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers=headers, loop=self.loop
            )
        return self._session

    def close(self):
        self.session.close()

    def add_url(self, url, sign, max_redirect=None):
        if max_redirect is None:
            max_redirect = self.max_redirect
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self.q.put_nowait((url, sign, max_redirect))

    @staticmethod
    async def picture(response):
        name = response.url.split(r'/')[-1]
        content = await response.read()
        if response.status == 200:
            async with aiofiles.open(name, 'wb') as f:
                await f.write(content)

    async def fetch(self, url, sign, max_redirect):
        print('I am fetching ', url)
        tries = 0
        while tries < self.max_tries:
            try:
                response = await self.session.get(
                    url, allow_redirects=False)
                break
            except aiohttp.ClientError:
                pass
        else:
            return

        try:
            if sign == 'link':
                await self.parse_link(response)
            elif sign == 'pic':
                await self.picture(response)
        finally:
            await response.release()

    async def parse_link(self, response):
        rs = await response.read()
        sel = etree.HTML(rs)
        urls = sel.xpath('//a[@class="view_img_link"]/@href')
        for url in urls:
            self.add_url('http:' + url, 'pic')
        next_page = sel.xpath('//a[@class="previous-comment-page"]/@href')
        if next_page:
            self.add_url(next_page[-1], 'link')

    async def work(self):
        try:
            while 1:
                url, sign, max_redirect = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url, sign, max_redirect)
                self.q.task_done()
                asyncio.sleep(0.5)
        except asyncio.CancelledError:
            pass

    async def crawl(self):
        worker = [asyncio.Task(self.work(), loop=self.loop) for _ in range(self.max_tasks)]
        self.time_start = datetime.now()
        await self.q.join()
        self.time_end = datetime.now()
        for w in worker:
            w.cancel()


if __name__ == '__main__':
    URL = 'http://jandan.net/ooxx'
    loop = asyncio.get_event_loop()
    crawler = Crawler()
    crawler.add_url(URL, 'link')
    loop.run_until_complete(crawler.crawl())
    print('Finished in {}'.format(crawler.time_end - crawler.time_start))
    print(len(crawler.seen_urls))
    crawler.close()
    loop.close()
