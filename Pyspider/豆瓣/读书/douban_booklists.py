import asyncio
import time
from asyncio import Queue
from urllib.parse import urljoin

import aiohttp
from datas import create_logging
from exchanges import messages
from faker import Factory
from lxml import etree

fake = Factory.create()


class Crawler(object):
    def __init__(self, max_tries=4, max_tasks=10, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        self.done = []
        self.t0 = time.time()
        self.t1 = None
        self._session = None

    def close(self):
        self.session.close()

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={'User-Agent': fake.user_agent(),
                         'Accept-Language': "zh-CN,zh"}, loop=self.loop)
        return self._session

    @staticmethod
    async def parse_link(response):
        rs = await response.read()
        booklist = etree.HTML(rs).xpath('//a/@href')
        booklist = [url for url in booklist if 'tag' in url and 'book' not in url]
        for book in booklist:
            print(urljoin('https://book.douban.com/tag/', book))
            await messages(urljoin('https://book.douban.com/tag/', book), 'tags')

    async def fetch(self, url):
        tries = 0
        while tries < self.max_tries:
            try:
                response = await self.session.get(
                    url, allow_redirects=False,
                    timeout=5)
                print(response.url)
                break
            except aiohttp.ClientError as client_error:
                logger.info(client_error)
            tries += 1
        else:
            return
        try:
            if response.status == 200:
                print(response.url, response.status)
                await self.parse_link(response)
            else:
                print(response.url, response.status)
        finally:
            await response.release()

    async def work(self):
        try:
            while 1:
                url = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url)
                self.q.task_done()
                asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

        except Exception as e:
            logger.info(e)
            logger.info(url)
            self.q.task_done()

    def add_url(self, url):
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self.q.put_nowait(url)

    async def crawl(self):
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        self.t0 = time.time()
        await self.q.join()
        self.t1 = time.time()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    logger = create_logging('豆瓣list', 'loggerlist.log')
    URL = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    loop = asyncio.get_event_loop()
    crawler = Crawler(max_tasks=10)
    crawler.add_url(URL)
    loop.run_until_complete(crawler.crawl())
    print('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))
    print('一共抓取网页--->', len(crawler.seen_urls))
    crawler.close()
    loop.close()
