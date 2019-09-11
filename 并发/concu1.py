import asyncio
import time

import aiohttp

NUMBERS = range(400)

URL = 'https://book.douban.com/tag/'

sema = asyncio.Semaphore(50)

start = time.time()


async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        data = await r.text()
        return r.status


async def print_result(a):
    with (await sema):
        r = await fetch_async(a)
        print('fetch({}) = {}'.format(a, r))


loop = asyncio.get_event_loop()
f = asyncio.wait([print_result(num) for num in NUMBERS])
loop.run_until_complete(f)
print(time.time() - start)
