import asyncio
from hashlib import sha224

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

url = "http://stackoverflow.com/feeds"


async def write_to_mongodb():
    client = AsyncIOMotorClient('localhost', 27017)
    db = client.mon
    collection = db.zufang

    house = {'_id': sha224(url.encode()).hexdigest(), 'apple': 'google'}
    try:
        await collection.insert(house)
    except DuplicateKeyError:
        print('error')


loop = asyncio.get_event_loop()
loop.run_until_complete(write_to_mongodb())
loop.close()
