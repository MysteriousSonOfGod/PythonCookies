from multiprocessing.dummy import Pool

import requests
from exchanges import message, receive
from faker import Factory
from lxml import etree

fake = Factory.create()


def fetch(ch, method, properties, body):
    url = body.decode()
    try:
        rs = requests.get(url, headers={'User-Agent': fake.user_agent()}, timeout=5)
        if rs.status_code == 200:
            parse_link(rs)
        else:
            print('something wrong...')

    except Exception as e:
        print(e)
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def parse_link(response):
    content = response.content
    selector = etree.HTML(content)
    urls = selector.xpath('//img/@src')
    urls = [url for url in urls if 'sinaimg' in url]
    if urls:
        for url in urls:
            message('img', url)
    else:
        pass


def main():
    receive(queue='link', func=fetch)


if __name__ == '__main__':
    pool = Pool(10)
    pool.apply_async(main)
    pool.close()
    pool.join()
