# coding=utf-8
import asyncio
import time

import aiohttp
from faker import Factory

NUMBERS = range(100)
# URL = 'http://www.baidu.com/?a={}'
URL = 'https://movie.douban.com/j/search_subjects?type=movie&tag=日本&sort=rank&page_limit=1&page_start={}'

fake = Factory.create()


async def fetch_async(a):
    header = {'User-Agent': fake.user_agent()}
    async with aiohttp.request('GET', URL.format(a), headers=header) as r:
        data = await r.text()
    return r.status


start = time.time()
event_loop = asyncio.get_event_loop()
tasks = [fetch_async(num) for num in NUMBERS]
results = event_loop.run_until_complete(asyncio.gather(*tasks))

# event_loop.close()

print('Use asyncio+aiohttp cost: {}'.format(time.time() - start))
