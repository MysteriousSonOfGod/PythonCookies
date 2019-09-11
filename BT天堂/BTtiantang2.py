# coding: utf-8

import random
import re
import time

import requests
from faker import Factory
from lxml import etree

start = time.time()

fake = Factory.create()

URL = 'http://www.bttt.la'
idpattern = re.compile(r'&id=(\d+)')
uhashpattern = re.compile(r'&uhash=(\w+)')
titlepattern = re.compile(r'/*')


def fetch(url):
    content = requests.get(url, headers={'User-Agent': fake.user_agent()}).content
    sel = etree.HTML(content)
    return sel


def getlist(link):
    sel = fetch(link)
    urls = sel.xpath('//div[@class="litpic"]/a[@target="_blank"]/@href')
    urls = [URL + url for url in urls]

    for url in urls:
        yield movie(url)

    nextpage = sel.xpath('//ul[@class="pagelist"]/li/a/text()')[-2]
    if nextpage == '下一页':
        yield getlist(URL + sel.xpath('//ul[@class="pagelist"]/li/a/@href')[-2])


def movie(url):
    sel = fetch(url)
    print(url)
    link = sel.xpath('//div[@class="tinfo"]/a/@href')
    infos = sel.xpath('//div[@class="tinfo"]/a/@title')
    if len(link) == len(infos):
        for i in range(len(link)):
            yield download(idpattern.search(link[i]).group(1), uhashpattern.search(link[i]).group(1), infos[i])


def download(id, uhash, title):
    title = titlepattern.sub('', title)
    MAINURL = ['http://www.bttt.la/download.php',
               'http://www.bttt.la/download2.php',
               'http://www.bttt.la/download3.php',
               'http://www.bttt.la/download4.php']

    data = {'action': 'download',
            'id': id,
            'download': 'd1',
            'uhash': uhash,
            'imageField.x': 100,
            'imageField.y': 30,
            }
    res = requests.post(MAINURL[random.randint(0, 3)], data=data, headers={'User-Agent': fake.user_agent()}).content

    with open(title + '.torrent', 'wb') as file:
        file.write(res)


if __name__ == '__main__':
    for il in getlist('http://www.bttt.la'):
        list(il)

    end = time.time()
    with open('cost.txt', 'w') as f:
        f.write(str(end - start))
