import asyncio
import base64
import codecs
import csv
import time
from asyncio import Queue

import requests
import ujson
from Crypto.Cipher import AES
from aiohttp import ClientSession, ClientError
from faker import Factory

fake = Factory.create()
file = 'comments.csv'


def create_csv():
    with open(file, 'w', ) as csvfile:
        fieldnames = ['用户', '评论', '时间']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


class Crawler(object):
    def __init__(self, musicID, max_tries=4, max_tasks=10, loop=None):
        self.musicID = musicID
        self.loop = loop or asyncio.get_event_loop()
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.t0 = time.time()
        self.t1 = None
        self._session = None

    @property
    def session(self):
        headers = {'User-Agent': fake.user_agent(),
                   'Cookie': 'appver=1.5.0.75771;',
                   'Referer': 'http://music.163.com/'
                   }
        if self._session is None:
            self._session = ClientSession(
                headers=headers, loop=self.loop)
        return self._session

    def close(self):
        self.session.close()

    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token="
    pubKey = "010001"
    modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    nonce = "0CoJUm6Qyw8W8jud"

    @staticmethod
    def write_to_csv(house_dict):
        with open(file, 'a+', encoding='utf8') as csvfile:
            fieldnames = ['用户', '评论', '时间']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(house_dict)

    def fetchNum(self):
        api = {'rid': 'R_SO_4_' + self.musicID, 'offset': '0', 'total': 'true', 'limit': '100', 'csrf_token': ''}
        _api = ujson.dumps(api)
        encText = self.aesEncrypt(self.aesEncrypt(_api, self.nonce), 16 * 'F')
        encSecKey = self.rsaEncrypt(16 * 'F', self.pubKey, self.modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        resp = requests.post(self.url.format(self.musicID), data=data).json()
        total = resp['total']
        return total

    @staticmethod
    def aesEncrypt(text, seckey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(seckey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        ciphertext = ciphertext.decode()
        return ciphertext

    @staticmethod
    def rsaEncrypt(text, pubKey, modulus):
        text = text[::-1]
        text = text.encode()
        rs = int(codecs.encode(text, 'hex').decode(), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    async def fetch_info(self, response):
        try:
            rs = await response.json()
            for item in rs['comments']:
                comments = dict()
                comments['用户'] = item['commentId']
                comments['评论'] = item['content']
                timeNow = int(str(item['time'])[0: -3])
                timeLocal = time.localtime(timeNow)
                comments['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
                self.write_to_csv(comments)
                print(item['content'])
        except Exception as error:
            print(error)

    async def fetch(self, num):
        tries = 0
        api = {'rid': 'R_SO_4_' + self.musicID, 'offset': str((num - 1) * 100), 'total': 'true', 'limit': '100',
               'csrf_token': ''}
        _api = ujson.dumps(api)
        encText = self.aesEncrypt(self.aesEncrypt(_api, self.nonce), 16 * 'F')
        encSecKey = self.rsaEncrypt(16 * 'F', self.pubKey, self.modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        while tries < self.max_tries:
            try:
                response = await self.session.post(self.url.format(self.musicID), data=data)
                break
            except ClientError:
                pass
            tries += 1
        else:
            return
        try:
            if response.status == 200:
                await self.fetch_info(response)
        finally:
            await response.release()

    async def work(self):
        try:
            while 1:
                num = await self.q.get()
                await self.fetch(num)
                self.q.task_done()
        except asyncio.CancelledError:
            pass

    def add_url(self, url):
        self.q.put_nowait((url))

    async def crawl(self):
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        self.t0 = time.time()
        await self.q.join()
        self.t1 = time.time()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    create_csv()
    loop = asyncio.get_event_loop()
    crawler = Crawler('186016', max_tasks=20)
    total = crawler.fetchNum()
    nums = int(total / 100) + 2
    URL = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token="
    for num in range(1, nums):
        crawler.add_url(num)
    loop.run_until_complete(crawler.crawl())
    print('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))
    crawler.close()
    loop.close()
