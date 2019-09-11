import asyncio
import csv
import time
from asyncio import Queue

import aiohttp
from faker import Factory
from lxml import etree

fake = Factory.create()
file = 'lianjia_gz.csv'


def create_csv():
    with open(file, 'w', ) as csvfile:
        fieldnames = ['链接', '面积', '房屋户型', '楼层', '房屋朝向', '地铁',
                      '小区', '位置', '时间', '租赁方式', '付款方式', '房屋现状',
                      '租赁周期', '装修描述', '小区介绍', '学区介绍', '核心卖点',
                      '周边配套', '交通出行', '户型介绍', '投资分析']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


class Crawler(object):
    def __init__(self, max_redirect=10, max_tries=4,
                 max_tasks=10, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        self.t0 = time.time()
        self.t1 = None
        self._session = None

    @property
    def session(self):
        headers = {'User-Agent': fake.user_agent()}
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers=headers, loop=self.loop)
        return self._session

    def close(self):
        self.session.close()

    @staticmethod
    def write_to_csv(house_dict):
        with open(file, 'a+', encoding='utf8') as csvfile:
            fieldnames = ['链接', '面积', '房屋户型', '楼层', '房屋朝向', '地铁',
                          '小区', '位置', '时间', '租赁方式', '付款方式', '房屋现状',
                          '租赁周期', '装修描述', '小区介绍', '学区介绍', '核心卖点',
                          '周边配套', '交通出行', '户型介绍', '投资分析']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(house_dict)

    async def parse_link(self, response):
        rs = await response.read()
        if response.status == 200:
            selector = etree.HTML(rs)
            urls = selector.xpath('//div[@class="info-panel"]/h2/a/@href')
            if urls is not None:
                for url in urls:
                    self.add_url(url, 'second')

    async def fetch_info(self, response):
        rs = await response.read()
        if response.status == 200:
            selector = etree.HTML(rs)
            house = dict()
            house['链接'] = response.url
            il = selector.xpath('//div[@class="zf-room"]/p/text()')
            house['面积'] = il[0]
            house['房屋户型'] = il[1]
            house['楼层'] = il[2]
            house['房屋朝向'] = il[3]
            house['地铁'] = il[4]
            il2 = selector.xpath('//div[@class="zf-room"]/p/a/text()')
            house['小区'] = ''.join(il2[:2])
            house['位置'] = ''.join(il2[2:])
            house['时间'] = il[-1]
            il3 = selector.xpath('//div[@class="base"]/div[@class="content"]/ul/li/text()')
            il3 = [i for i in map(str.strip, il3) if i != '']
            if len(il3) == 4:
                house['租赁方式'] = il3[0]
                house['付款方式'] = il3[1]
                house['房屋现状'] = il3[2]
                house['租赁周期'] = il3[3]
            else:
                house['租赁方式'] = '没抓取成功'
                house['付款方式'] = '没抓取成功'
                house['房屋现状'] = '没抓取成功'
                house['租赁周期'] = '没抓取成功'
            il4 = selector.xpath('//div[@class="featureContent"]/ul/li')
            for i in il4:
                house[i.xpath('span[@class="label"]/text()')[0][:-1].strip()] \
                    = i.xpath('span[@class="text"]/text()')[0]
            self.write_to_csv(house)

    async def fetch(self, url, sign, max_redirect):
        print('I am fetching ', url)
        tries = 0
        while tries < self.max_tries:
            try:
                response = await self.session.get(
                    url, allow_redirects=False
                )
                break
            except aiohttp.ClientError:
                pass
            tries += 1
        else:
            return

        try:
            if sign == 'first':
                await self.parse_link(response)
            elif sign == 'second':
                await self.fetch_info(response)
        finally:
            await response.release()

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

    def add_url(self, url, sign, max_redirect=None):
        if max_redirect is None:
            max_redirect = self.max_redirect
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self.q.put_nowait((url, sign, max_redirect))

    async def crawl(self):
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        self.t0 = time.time()
        await self.q.join()
        self.t1 = time.time()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    create_csv()
    URL = 'http://gz.lianjia.com/zufang/pg{}/'
    loop = asyncio.get_event_loop()
    crawler = Crawler()
    for num in range(1, 101):
        crawler.add_url(URL.format(num), 'first')
    loop.run_until_complete(crawler.crawl())
    print('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))
    print(len(crawler.seen_urls))
    crawler.close()
    loop.close()
