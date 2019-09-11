import asyncio

import asynqp

RECONNECT_BACKOFF = 1


class Consumer(object):
    def __init__(self, connection, queue):
        self.queue = queue
        self.connection = connection

    def __call__(self, msg):
        self.queue.put_nowait(msg)

    def on_error(self, exc):
        print("Connection lost while consuming queue", exc)


async def connect_and_consume(queue, types):
    connection = await asynqp.connect()
    try:
        channel = await connection.open_channel()

        amqp_queue = await channel.declare_queue('douban_{}.queue'.format(types))
        consumer = Consumer(connection, queue)
        await amqp_queue.consume(consumer)
    except asynqp.AMQPError as err:
        print("Could not consume on queue", err)
        await connection.close()
        return None
    return connection


async def reconnector(queue, types):
    try:
        connection = None
        while 1:
            if connection is None or connection.is_closed():
                print("Connecting to rabbitmq...")

                try:
                    connection = await connect_and_consume(queue, types)
                except (ConnectionError, OSError):
                    print("Failed to connect to rabbitmq server. Will retry in {} seconds".format(RECONNECT_BACKOFF))
                    connection = None
                if connection is None:
                    await asyncio.sleep(RECONNECT_BACKOFF)
                else:
                    print("Successfully connected and consuming douban_{}.queue".format(types))
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        if connection is not None:
            await connection.close()


async def messages(mess, types):
    connection = await asynqp.connect()
    channel = await connection.open_channel()
    exchange = await channel.declare_exchange('douban_{}.exchange'.format(types), 'direct')
    queue = await channel.declare_queue('douban_{}.queue'.format(types))
    await queue.bind(exchange, 'routing.key')
    msg = asynqp.Message(mess)
    exchange.publish(msg, 'routing.key')
    await channel.close()
    await connection.close()
