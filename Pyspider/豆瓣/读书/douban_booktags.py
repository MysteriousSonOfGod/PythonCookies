import asyncio
from urllib.parse import urljoin

import aiohttp
from datas import create_logging
from exchanges import messages, reconnector
from faker import Factory
from lxml import etree

fake = Factory.create()


class Crawler(object):
    def __init__(self, max_tries=4, max_tasks=10, loop=asyncio.get_event_loop(), queue=asyncio.Queue()):
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.loop = loop
        self.queue = queue
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={'User-Agent': fake.user_agent(),
                         'Accept-Language': "zh-CN,zh"}, loop=self.loop)
        return self._session

    async def fetch(self, url):
        tries = 0
        while tries < self.max_tries:
            try:
                response = await self.session.get(url.decode(), allow_redirects=False)
                break
            except aiohttp.ClientError as client_error:
                logger.info(client_error)
            tries += 1
        else:
            return
        try:
            if response.status == 200:
                print(response.url, 200)
                await self.book_tag(response)
            else:
                print(response.url, response.status)
        finally:
            await response.release()

    @staticmethod
    async def book_tag(response):
        response_url = str(response.url)
        rs = await response.read()
        selector = etree.HTML(rs)
        tags = selector.xpath('//h2[@class=""]/a/@href')
        for tag in tags:
            await messages(tag, 'items')
        next_page = selector.xpath('//span[@class="next"]/link/@href')
        if next_page:
            await messages(urljoin(response_url, next_page[0]), 'tags')

    async def process_msgs(self, queue):
        try:
            while 1:
                msg = await queue.get()
                await self.fetch(msg.body)
                msg.ack()
                self.queue.task_done()
        except asyncio.CancelledError:
            pass

        except Exception as e:
            self.queue.task_done()
            raise

    def run(self):
        reconnect_task = self.loop.create_task(reconnector(self.queue, 'tags'))
        process_task = [self.loop.create_task(self.process_msgs(self.queue)) for _ in range(self.max_tasks)]
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            process_task.cancel()
            reconnect_task.cancel()
            self.loop.run_until_complete(process_task)
            self.loop.run_until_complete(reconnect_task)
        self.loop.close()


if __name__ == "__main__":
    crawl = Crawler(max_tasks=1)
    logger = create_logging('豆瓣tag', 'loggertag.log')
    crawl.run()
