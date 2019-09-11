import asyncio
from collections import OrderedDict

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.test_database
collection = db.test_collection2

house = OrderedDict()
house['a'] = 1
house['b'] = 2
house['c'] = 3
house['d'] = 4


async def do_insert():
    await collection.insert(house)


loop = asyncio.get_event_loop()
loop.run_until_complete(do_insert())
