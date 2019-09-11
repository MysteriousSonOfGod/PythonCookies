import asyncio

import aiohttp
from datas import create_logging
from datas import write_to_csv
from exchanges import reconnector
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
                print(response.url, response.status)
                await self.book_item(response)
            else:
                pass
        finally:
            await response.release()

    @staticmethod
    async def book_item(response):
        rs = await response.read()
        selector = etree.HTML(rs)
        books = dict()
        try:
            books['书名'] = selector.xpath('//h1/span/text()')[0]
            author = selector.xpath('//div[@id="info"]/a/text()')
            books['作者'] = [il for il in map(str.strip, [author[0]])][0]
            rate = selector.xpath('//div[contains(@class,"clearfix")]/strong/text()')
            if rate:
                books['豆瓣评分'] = rate[0]
            else:
                pass
            contents = selector.xpath('//div[@class="intro"]')
            texts = []
            for content in contents:
                texts.append(content.xpath('p/text()'))
            if len(texts) == 1:
                content = ''.join(texts[0])
            else:
                if texts[0][0] == texts[1][0]:
                    content = texts[1]
                else:
                    content = texts[0]
                content = ''.join(content)
            books['简介'] = content
        except Exception as e:
            books['书名'] = None
            books['作者'] = None
            books['豆瓣评分'] = None
            books['简介'] = None
        finally:
            write_to_csv(books)

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
        reconnect_task = self.loop.create_task(reconnector(self.queue, 'items'))
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
    crawl = Crawler(max_tasks=10)
    logger = create_logging('豆瓣item', 'loggeritem.log')
    crawl.run()
