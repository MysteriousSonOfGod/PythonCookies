# coding: utf-8

import csv
import time
from collections import OrderedDict

import requests
from faker import Factory
from lxml import etree

URL = 'https://book.douban.com/tag/'
fake = Factory.create()

mainURL = 'https://book.douban.com'

start = time.time()


def get(url):
    header = {'User-Agent': fake.user_agent()}
    r = requests.get(url, headers=header)
    return r.text


def run():
    booklist = etree.HTML(get(URL))
    booklist = booklist.xpath('//a/@href')
    booklist = [url for url in booklist if 'tag' in url and 'book' not in url]
    for il in booklist:
        yield book(mainURL + il)


def book(url):
    print(url)
    text = etree.HTML(get(url))
    il = text.xpath('//li[@class="subject-item"]')
    if il:
        for i in il:
            d = OrderedDict()
            d['title'] = i.xpath('div[@class="info"]/h2/a/@title')[0]
            try:
                d['rate'] = i.xpath('div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[
                    0]
            except IndexError:
                d['rate'] = 'None'
            d['url'] = i.xpath('div[@class="info"]/h2/a/@href')[0]
            with open('books.csv', 'a+', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(list(d.values()))

            nextpage = text.xpath('//span[@class="next"]/a/@href')
            if nextpage:
                return book(mainURL + nextpage[0])


if __name__ == '__main__':
    with open('books.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['title', 'rate', 'url'])

    list(run())

    with open('cost.txt', 'w') as f:
        f.write(str((time.time() - start)))
