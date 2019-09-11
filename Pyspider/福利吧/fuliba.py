import time
from multiprocessing.dummy import Pool
from queue import Queue

import requests
from faker import Factory
from lxml import etree

start = time.time()

fake = Factory.create()

URL = 'http://fuliba.net/page/{}'  # 1-122

URI = Queue()


def main():
    while not URI.empty():
        url, sign = URI.get_nowait()
        try:
            rs = requests.get(url, headers={'User-Agent': fake.user_agent()}, timeout=5)
            if rs.status_code == 200:
                if sign == 'first':
                    parse(rs)
                elif sign == 'second':
                    parse_link(rs)
                elif sign == 'img':
                    images(rs)
        except Exception as e:
            print(e)


def parse(response):
    print(response.url)
    content = response.content
    selector = etree.HTML(content)
    urls = selector.xpath('//article/header/h2/a/@href')
    if urls:
        for url in urls:
            URI.put_nowait((url, 'second'))


def parse_link(response):
    print(response.url)
    content = response.content
    selector = etree.HTML(content)
    urls = selector.xpath('//img/@src')
    urls = [url for url in urls if 'sinaimg' in url]
    if urls:
        for url in urls:
            URI.put_nowait((url, 'img'))


def images(response):
    print(response.url)
    content = response.content
    try:
        with open(response.url.split(r'/')[-1], 'wb') as img:
            img.write(content)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pool = Pool(10)
    for num in range(1, 98):
        URI.put_nowait((URL.format(num), 'first'))
    pool.apply(main)
    pool.close()
    pool.join()
    print(time.time() - start)
