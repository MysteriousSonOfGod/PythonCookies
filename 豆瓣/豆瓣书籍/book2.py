# coding: utf-8

import csv
from collections import OrderedDict
from datetime import datetime
from threading import Thread, Semaphore

import requests
from faker import Factory
from lxml import etree

fake = Factory.create()
sema = Semaphore(10)

URL = 'https://book.douban.com/tag/'
mainURL = 'https://book.douban.com'

start = datetime.now()
with open('cost.txt', 'a+') as t:
    t.write(str(start) + '\n')


def get(url):
    header = {'User-Agent': fake.user_agent()}
    try:
        cookie = {'name': '__pk_ref.100001.3ac3', 'value': 'a4c24adbcdf9528e.1482319141.7.1482505484.1482465002.',
                  'domain': 'book.douban.com', 'path': '/'}

        r = requests.get(url, headers=header, cookies=cookie, timeout=3)
        return r.content
    except:
        with open('error.txt', 'a+', encoding='utf-8') as er:
            er.write(url + '解析失败' + '\n')


threads = []


def run():
    #  File "src\lxml\lxml.etree.pyx", line 3161, in lxml.etree.HTML (src\lxml\lxml.etree.c:78427)
    #   File "src\lxml\parser.pxi", line 1847, in lxml.etree._parseMemoryDocument (src\lxml\lxml.etree.c:118298)
    #  ValueError: can only parse strings
    booklist = etree.HTML(get(URL))
    booklist = booklist.xpath('//a/@href')
    booklist = [url for url in booklist if 'tag' in url and 'book' not in url]
    with open('total.txt', 'w') as t:
        t.write(str(len(booklist)) + '\n')

    with sema:
        for il in booklist:
            t = Thread(target=book, args=(mainURL + il,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


def book(url):
    #  File "src\lxml\lxml.etree.pyx", line 3161, in lxml.etree.HTML (src\lxml\lxml.etree.c:78427)
    #   File "src\lxml\parser.pxi", line 1847, in lxml.etree._parseMemoryDocument (src\lxml\lxml.etree.c:118298)
    #  ValueError: can only parse strings
    print(url)
    try:
        text = etree.HTML(get(url))
        il = text.xpath('//li[@class="subject-item"]')
        if il:
            for i in il:
                d = OrderedDict()
                d['title'] = i.xpath('div[@class="info"]/h2/a/@title')[0]
                try:
                    d['rate'] = \
                        i.xpath('div[@class="info"]/div[@class="star clearfix"]/span[@class="rating_nums"]/text()')[0]
                except IndexError:
                    d['rate'] = 'None'
                d['url'] = i.xpath('div[@class="info"]/h2/a/@href')[0]
                with open('books1.csv', 'a+', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow(list(d.values()))

                nextpage = text.xpath('//span[@class="next"]/a/@href')
                if nextpage:
                    return book(mainURL + nextpage[0])

    except:
        with open('error.txt', 'a+', encoding='utf-8') as er:
            er.write(url + '分析信息失败' + '\n')


if __name__ == '__main__':
    with open('books.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['title', 'rate', 'url'])

    run()

    end = datetime.now()
    with open('cost.txt', 'a+') as f:
        f.write(str((datetime.now() - start)))
