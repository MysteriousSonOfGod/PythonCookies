import asyncio
import time

import aiohttp
import ujson
import uvloop
from faker import Factory
from lxml import etree

fake = Factory.create()
start = time.time()

sema = asyncio.Semaphore(3)

start = time.time()

URL = 'https://movie.douban.com/top250'


async def fetch(url):
    headers = {'User-Agent': fake.user_agent()}
    async with aiohttp.request('GET', url, headers=headers) as res:
        if res.status == 200:
            print(url)
            return await res.read()
        else:
            with open('failed.txt', 'a') as error:
                error.write(url + '\n')
                return None


async def selector(url):
    with (await sema):
        content = await fetch(url)
        if content:
            sel = etree.HTML(content)
            return sel
        else:
            return None


async def produce(queue, url):
    with (await sema):
        sel = await selector(url)
        movies = sel.xpath('//div[@class="hd"]/a/@href')
        for movie in movies:
            await queue.put(movie)


async def worker(url):
    print('I am working--->', url)
    with (await sema):
        sel = await selector(url)
        if sel:
            info = {}
            info['title'] = sel.xpath('//span[@property="v:itemreviewed"]/text()')[0]
            info['rate'] = sel.xpath('//strong[@class="ll rating_num"]/text()')[0]
            info['nums'] = sel.xpath('//span[@property="v:votes"]/text()')[0]
            info['director'] = sel.xpath('//*[@rel="v:directedBy"]/text()')[0]
            info['content'] = ''.join(sel.xpath('//*[@property="v:summary"]/text()'))
            json_dict = ujson.dumps(info, ensure_ascii=0)
            print(json_dict)
            with open('top250.txt', 'a', encoding='utf-8') as f:
                f.write(json_dict)


async def consume(queue):
    while 1:
        item = await queue.get()
        await worker(item)
        queue.task_done()


async def run():
    queue = asyncio.PriorityQueue()
    consumer = asyncio.ensure_future(consume(queue))
    await produce(queue, URL)
    await queue.join()
    consumer.cancel()


# loop = asyncio.get_event_loop()
loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(run())
loop.close()

print(time.time() - start)
