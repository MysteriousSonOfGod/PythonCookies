from redis import Redis
from rq import Queue
from work import fetch

q = Queue(connection=Redis())
URL = 'https://www.baidu.com/?a={}'
for i in range(20):
    q.enqueue(fetch, URL.format(i))
