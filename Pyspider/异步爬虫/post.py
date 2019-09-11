import asyncio

import aiohttp


async def fetch(session, url):
    with aiohttp.Timeout(10):
        async with session.post(url, data={'action': 'download',
                                           'down': 'dl',
                                           'id': '29016',
                                           'uhash': 'f9f9c0d674b2a64d03e76b1d',
                                           'imageField.x': '84',
                                           'imageField.y': '35'}) as response:
            data = await response.read()
            with open('test.torrent', 'wb') as f:
                f.write(data)


async def main(loop, url):
    async with aiohttp.ClientSession(loop=loop) as session:
        return await fetch(session, url)


url = 'http://www.bttt.la/download.php'
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, url))
