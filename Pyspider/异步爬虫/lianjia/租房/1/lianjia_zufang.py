import asyncio
import logging
import time
from asyncio import Queue

import aiohttp
import asynqp
from faker import Factory
from lxml import etree

fake = Factory.create()

fieldnames = ['链接', '价格', '面积', '房屋户型', '楼层', '房屋朝向', '地铁',
              '小区', '位置', '时间', '租赁方式', '付款方式', '房屋现状',
              '租赁周期|供暖方式', '装修描述', '小区介绍', '学区介绍', '核心卖点',
              '周边配套', '交通出行', '户型介绍', '投资分析', '出租原因',
              '房源亮点']


def create_logging(logger_name, logger_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handle_write = logging.FileHandler(logger_file)
    handle_print = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    handle_print.setFormatter(formatter)
    handle_write.setFormatter(formatter)
    logger.addHandler(handle_print)
    logger.addHandler(handle_write)
    return logger


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

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={'User-Agent': fake.user_agent()}, loop=self.loop)
        return self._session

    def close(self):
        self.session.close()

    @staticmethod
    async def message(mess):
        connection = await asynqp.connect()
        channel = await connection.open_channel()
        exchange = await channel.declare_exchange('lianjia_zufang.exchange', 'direct')
        queue = await channel.declare_queue('lianjia_zufang.queue')
        await queue.bind(exchange, 'routing.key')
        msg = asynqp.Message(mess)
        exchange.publish(msg, 'routing.key')
        await channel.close()
        await connection.close()

    async def parse_link(self, response):
        rs = await response.read()
        if response.status == 200:
            selector = etree.HTML(rs)
            urls = selector.xpath('//div[@class="info-panel"]/h2/a/@href')
            if urls:
                for url in urls:
                    if 'sh.lianjia.com' in response.url:
                        await self.message('http://sh.lianjia.com' + url)
                    else:
                        await self.message(url)

    async def fetch(self, url):
        tries = 0
        while tries < self.max_tries:
            try:
                response = await self.session.get(url, allow_redirects=False)
                break
            except aiohttp.ClientError as client_error:
                logger.info(client_error)
            tries += 1
        else:
            return
        try:
            print(response.url, response.status)
            await self.parse_link(response)
        finally:
            await response.release()

    async def work(self):
        try:
            while 1:
                url = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url)
                self.q.task_done()
                asyncio.sleep(5)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.info(e)
            logger.info(url)
            self.q.task_done()

    def add_url(self, url):
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self.q.put_nowait((url))

    async def crawl(self):
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        self.t0 = time.time()
        await self.q.join()
        self.t1 = time.time()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    logger = create_logging('链家爬虫', 'logger.log')
    # 琼海没有信息
    # 苏州没有信息
    # 石家庄没有信息
    # 沈阳没有信息
    # 三亚没有信息
    # 文昌没有信息
    # 万宁没有信息
    # 海口没有信息
    # 西安没有信息
    # 陵水没有信息
    # 廊坊燕郊没有信息
    URLs = ['http://bj.lianjia.com/zufang/pg{}/', 'http://nj.lianjia.com/zufang/pg{}/',
            'http://cd.lianjia.com/zufang/pg{}/', 'http://cq.lianjia.com/zufang/pg{}/',
            'http://cs.lianjia.com/zufang/pg{}/', 'http://qd.lianjia.com/zufang/pg{}/',
            'http://dl.lianjia.com/zufang/pg{}/', 'http://dg.lianjia.com/zufang/pg{}/',
            'http://sh.lianjia.com/zufang/d{}/', 'http://sz.lianjia.com/zufang/pg{}/',
            'http://fs.lianjia.com/zufang/pg{}/', 'http://tj.lianjia.com/zufang/pg{}/',
            'http://gz.lianjia.com/zufang/pg{}/', 'http://wh.lianjia.com/zufang/pg{}/',
            'http://hz.lianjia.com/zufang/pg{}/', 'http://hf.lianjia.com/zufang/pg{}/',
            'http://xm.lianjia.com/zufang/pg{}/', 'http://jn.lianjia.com/zufang/pg{}/',
            'http://yt.lianjia.com/zufang/pg{}/', 'http://zs.lianjia.com/zufang/pg{}/',
            'http://zh.lianjia.com/zufang/pg{}/'
            ]
    loop = asyncio.get_event_loop()
    crawler = Crawler(max_tasks=3)
    for URL in URLs:
        for num in range(1, 101):
            crawler.add_url(URL.format(num))
    # crawler.add_url('http://gz.lianjia.com/zufang/pg2/') #测试
    loop.run_until_complete(crawler.crawl())
    print('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))
    print('一共抓取网页--->', len(crawler.seen_urls))
    crawler.close()
    loop.close()
