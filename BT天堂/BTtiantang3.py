import asyncio
import time

import aiohttp
import async_timeout
from faker import Factory
from lxml import etree

fake = Factory.create()
start = time.time()
URL = 'http://www.bttt.la/'
sema = asyncio.Semaphore(3)


async def fetch(url):
    print('fetch------->')
    headers = {'User-Agent': fake.user_agent()}
    with async_timeout.timeout(10):
        async with aiohttp.request('GET', url, headers=headers) as r:
            data = await r.read()
        return data


async def selector(url):
    print('selector----------')
    with (await sema):
        content = await fetch(url)
        sel = etree.HTML(content)
        return sel


async def collect_result(url):
    print('collect_result----->')
    with (await sema):
        sel = await selector(url)
        urls = sel.xpath('//div[@class="litpic"]/a/@href')
        return urls


async def produce(queue, url):
    print('produce-----')
    with (await sema):
        urls = await collect_result(url)
        for url in urls:
            await queue.put(url)


async def consume(queue):
    print('consume-------')
    while 1:
        item = await queue.get()
        sel = await selector('http://www.bttt.la' + item)
        movies = sel.xpath('//div[@class="tinfo"]/a/@href')
        with open('links.txt', 'a') as f:
            for movie in movies:
                f.write(movie + '\n\n')
        queue.task_done()


async def run():
    print('run---------')
    queue = asyncio.PriorityQueue()
    consumer = asyncio.ensure_future(consume(queue))
    await produce(queue, URL)
    await queue.join()
    consumer.cancel()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()

print(time.time() - start)
