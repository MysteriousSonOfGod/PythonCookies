import asyncio
import csv
from collections import OrderedDict
from datetime import datetime

import aiohttp
from faker import Factory
from lxml import etree

URL = 'https://book.douban.com/tag/'
mainURL = 'https://book.douban.com'
fake = Factory.create()
start = datetime.now()

with open('cost.txt', 'a+') as t:
    t.write(str(start) + '\n')

sema = asyncio.Semaphore(20)


async def fetch(url):
    header = {'User-Agent': fake.user_agent()}
    async with aiohttp.request('GET', url, headers=header, encoding='utf-8') as res:
        data = await res.text()
        return data


async def book_list():
    book = await fetch(URL)
    booklist = etree.HTML(book).xpath('//a/@href')
    booklist = [url for url in booklist if 'tag' in url and 'book' not in url]
    for il in booklist:
        await books(mainURL + il)


async def books(url):
    text = await etree.HTML(fetch(url))
    lists = text.xpath('//li[@class="subject-item"]')
    if lists:
        for i in lists:
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
                return books(mainURL + nextpage[0])


loop = asyncio.get_event_loop()
f = asyncio.wait([book_list()])
loop.run_until_complete(f)

end = datetime.now()

with open('cost.txt', 'a+') as t:
    t.write(str(start - end) + '\n')
