import asyncio
import time

import aiohttp

NUMBERS = range(50)

URL = 'https://www.baidu.com/?a={}'


async def fetch_async(a):
    async with aiohttp.request('GET', URL.format(a)) as r:
        return r.status


start = time.time()
event_loop = asyncio.get_event_loop()
tasks = [fetch_async(num) for num in NUMBERS]
results = event_loop.run_until_complete(asyncio.gather(*tasks))
for num, result in zip(NUMBERS, results):
    print('fetch({}) = {}'.format(num, result))

print('Use asyncio+aiohttp cost: {}'.format(time.time() - start))
