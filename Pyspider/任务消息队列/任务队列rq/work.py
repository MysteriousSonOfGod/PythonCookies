import redis
import requests
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']
redis_url = 'redis://localhost:6379'
conn = redis.from_url(redis_url)


def fetch(url):
    print('fetching {}'.format(url))
    rs = requests.get(url)
    return rs.content


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
