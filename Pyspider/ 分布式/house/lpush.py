import redis

try:
    r = redis.StrictRedis(host='localhost', port=6379)
    r.lpush('anjuke:anjuke_urls', 'http://gz.zu.anjuke.com/fangyuan/p1/')
except Exception as e:
    print(e)
