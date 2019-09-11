import asyncio
import csv
import logging

import aiohttp
import asynqp
from faker import Factory
from lxml import etree
from motor import motor_asyncio

RECONNECT_BACKOFF = 1

fake = Factory.create()
file = 'lianjia_zufang.csv'

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


class Consumer(object):
    def __init__(self, connection, queue):
        self.queue = queue
        self.connection = connection

    def __call__(self, msg):
        self.queue.put_nowait(msg)

    def on_error(self, exc):
        print("Connection lost while consuming queue", exc)


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
                headers={'User-Agent': fake.user_agent()}, loop=self.loop)
        return self._session

    @staticmethod
    def write_to_csv(house_dict):
        with open(file, 'a+', encoding='utf8') as csvfile:
            global fieldnames
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(house_dict)

    @staticmethod
    async def write_to_mongodb(house):
        await collection.insert(house)

    @staticmethod
    async def connect_and_consume(queue):
        connection = await asynqp.connect()
        try:
            channel = await connection.open_channel()
            amqp_queue = await channel.declare_queue('lianjia_zufang.queue')
            consumer = Consumer(connection, queue)
            await amqp_queue.consume(consumer)
        except asynqp.AMQPError as err:
            print("Could not consume on queue", err)
            await connection.close()
            return None
        return connection

    async def reconnector(self, queue):
        try:
            connection = None
            while 1:
                if connection is None or connection.is_closed():
                    print("Connecting to rabbitmq...")
                    try:
                        connection = await self.connect_and_consume(queue)
                    except (ConnectionError, OSError):
                        print(
                            "Failed to connect to rabbitmq server. Will retry in {} seconds".format(RECONNECT_BACKOFF))
                        connection = None
                    if connection is None:
                        await asyncio.sleep(RECONNECT_BACKOFF)
                    else:
                        print("Successfully connected and consuming lianjia_zufang.queue")
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            if connection is not None:
                await connection.close()

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
            print(response.url, response.status)
            await self.fetch_info(response)
        finally:
            await response.release()

    async def fetch_info(self, response):
        rs = await response.read()
        if response.status == 200:
            selector = etree.HTML(rs)
            try:
                house = dict()
                house['链接'] = response.url
                house['价格'] = selector.xpath('//span[@class="total"]/text()')[0]
                il = selector.xpath('//div[@class="zf-room"]/p/text()')
                if il:
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
                        house['租赁周期|供暖方式'] = il3[3]
                    elif len(il3) == 3:
                        il3 = selector.xpath('//div[@class="base"]/div[@class="content"]/ul/li')
                        house['租赁方式'] = il3[0].xpath('text()')[0]
                        house['付款方式'] = il3[1].xpath('a/text()')[0]
                        house['房屋现状'] = il3[2].xpath('text()')[0]
                        house['租赁周期|供暖方式'] = il3[3].xpath('text()')[0]
                    else:
                        house['租赁方式'] = '没抓取成功'
                        house['付款方式'] = '没抓取成功'
                        house['房屋现状'] = '没抓取成功'
                        house['租赁周期'] = '没抓取成功'
                    il4 = selector.xpath('//div[@class="featureContent"]/ul/li')
                    try:
                        for i in il4:
                            house[i.xpath('span[@class="label"]/text()')[0][:-1].strip()] \
                                = i.xpath('span[@class="text"]/text()')[0]
                    except IndexError:
                        for i in range(len(il4)):
                            if i == 0:
                                house[il4[i].xpath('span[@class="label"]/text()')[0][:-1].strip()] \
                                    = il4[i].xpath('span[@class="text"]/span/text()')[0]
                            else:
                                house[il4[i].xpath('span[@class="label"]/text()')[0][:-1].strip()] \
                                    = il4[i].xpath('span[@class="text"]/text()')[0]
                    self.write_to_csv(house)
                    await self.write_to_mongodb(house)
            except Exception as e:
                logger.info(e)
                logger.info(response.url)

    async def process_msgs(self, queue):
        try:
            while 1:
                msg = await queue.get()
                # print(msg.body)
                await self.fetch(msg.body)
                msg.ack()
                asyncio.sleep(2)
        except asyncio.CancelledError:
            pass

    def run(self):
        reconnect_task = self.loop.create_task(self.reconnector(self.queue))
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
    client = motor_asyncio.AsyncIOMotorClient('localhost', 27017)
    db = client.lianjia
    collection = db.zufang
    logger = create_logging('链家爬虫', 'logger.log')
    crawl = Crawler(max_tasks=3)
    crawl.run()
