from multiprocessing.dummy import Pool

import requests
from exchanges import receive
from faker import Factory

fake = Factory.create()


def fetch(ch, method, properties, body):
    url = body.decode()
    try:
        rs = requests.get(url, headers={'User-Agent': fake.user_agent()}, timeout=5)
        if rs.status_code == 200:
            images(rs)
        else:
            print('somethig wrong...')
    except Exception as e:
        print(e)
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def images(response):
    print(response.url)
    content = response.content
    try:
        with open(response.url.split(r'/')[-1], 'wb') as img:
            img.write(content)
    except Exception as e:
        print(e)


def main():
    receive('img', fetch)


if __name__ == '__main__':
    pool = Pool(4)
    pool.apply_async(main)
    pool.close()
    pool.join()
