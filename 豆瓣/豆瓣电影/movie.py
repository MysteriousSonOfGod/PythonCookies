# coding: utf-8

import csv
import os
import sys
import time
from collections import OrderedDict
from itertools import count

import requests
from faker import Factory

URL = 'https://movie.douban.com/j/search_subjects?type=movie&tag={}&sort=rank&page_limit=20&page_start={}'

fake = Factory.create()
tag = sys.argv[1]

start = time.time()


def get(URL):
    header = {'User-Agent': fake.user_agent()}
    r = requests.get(URL, headers=header)
    return r.json()


def main():
    for num in count():
        js = get(URL.format(tag, 20 * num))
        content = js['subjects']
        if not content:
            break
        else:
            for text in content:
                item = OrderedDict()
                item['title'] = text['title']
                item['rate'] = text['rate']
                item['url'] = text['url']
                with open(sys.argv[1] + '.csv', 'a+') as f:
                    w = csv.writer(f)
                    w.writerow(list(item.values()))


if __name__ == '__main__':

    if os.path.isfile(sys.argv[1] + '.csv'):
        print('此命令已经运行过,程序结束')
    else:
        with open(sys.argv[1] + '.csv', 'w') as f:
            w = csv.writer(f)
            w.writerow(['title', 'rate', 'url'])

        main()
        print(time.time() - start)
