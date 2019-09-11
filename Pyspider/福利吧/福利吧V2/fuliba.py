import time
from multiprocessing.dummy import Pool
from queue import Queue

import requests
from exchanges import message
from faker import Factory
from lxml import etree

start = time.time()

fake = Factory.create()

URL = 'http://fuliba.net/page/{}'  # 1-98

URI = Queue()


def main():
    while not URI.empty():
        url = URI.get_nowait()
        try:
            rs = requests.get(url, headers={'User-Agent': fake.user_agent()}, timeout=5)
            if rs.status_code == 200:
                parse_link(rs)
            else:
                pass
        except Exception as e:
            print(e)


def parse_link(response):
    content = response.content
    selector = etree.HTML(content)
    urls = selector.xpath('//article/header/h2/a/@href')
    if urls:
        for url in urls:
            message('link', url)
    else:
        pass


if __name__ == '__main__':
    pool = Pool(10)
    for num in range(1, 2):
        URI.put_nowait(URL.format(num))
    pool.apply_async(main)
    pool.close()
    pool.join()
    print(time.time() - start)
