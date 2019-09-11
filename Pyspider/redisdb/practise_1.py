import asyncio

import asyncio_redis


def values(*value):
    for element in value:
        yield element


async def insert(loop, *args, keys='key'):
    print(args)
    transport, protocol = await loop.create_connection(
        asyncio_redis.RedisProtocol, '127.0.0.1', 6379)
    await protocol.lpush(keys, values(*args))
    # insert_values = await protocol.lrange('key', 0, -1)
    # insert_values = await insert_values.aslist()
    # print(insert_values)
    transport.close()


async def work():
    url = await pop(loop)
    while url:
        print('work', url)
        url = await pop()


async def pop(loop):
    transport, protocol = await loop.create_connection(
        asyncio_redis.RedisProtocol, '127.0.0.1', 6379)
    data = await protocol.lpop('key')
    print(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    URL = 'https://www.baidu.com/?a={}'
    li = [URL.format(i) for i in range(12)]
    loop.run_until_complete(pop(loop))
    loop.close()
