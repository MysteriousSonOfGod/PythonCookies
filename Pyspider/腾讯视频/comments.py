import asyncio
import csv
import time
from asyncio import Queue

import aiohttp
import ujson
from faker import Factory

fake = Factory.create()
file = '狐狸的夏天.csv'


def create_csv():
    with open(file, 'w', ) as csvfile:
        fieldnames = ['用户', '评论', '时间']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


class Crawler(object):
    def __init__(self, url_id, max_tries=2, max_tasks=10, loop=None):
        self.url_id = url_id
        self.loop = loop or asyncio.get_event_loop()
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = Queue(loop=self.loop)
        self.seen_urls = set()
        self.t0 = time.time()
        self.t1 = None
        self._session = None
        self.URL = 'https://coral.qq.com/article/{}'.format(url_id) + '/comment?commentid={}&reqnum=50'

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(headers={'User-Agent': fake.user_agent()}, loop=self.loop)
        return self._session

    def close(self):
        self.session.close()

    @staticmethod
    def write_to_csv(comment_dict):
        fieldnames = ['用户', '评论', '时间']
        with open(file, 'a+', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(comment_dict)

    async def fetch_info(self, response):
        rs = await response.text()
        rs = ujson.loads(rs)
        link = rs['data']['last']
        if type(link) == str:
            self.add_url(self.URL.format(link))
        try:
            comments = rs['data']['commentid']
            for comment in comments:
                user_comments = dict()
                user_comments['用户'] = comment['userid']
                user_comments['评论'] = comment['content']
                time_local = time.localtime(comment['time'])
                user_comments['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                self.write_to_csv(user_comments)
        except Exception as e:
            print(e)

    async def fetch(self, url):
        tries = 0
        while tries < self.max_tries:
            try:
                response = await self.session.get(url, allow_redirects=False)
                break
            except aiohttp.ClientError:
                pass
            tries += 1
        else:
            return

        try:
            if response.status == 200:
                print(url)
                await self.fetch_info(response)
            else:
                pass
        finally:
            await response.release()

    async def work(self):
        try:
            while 1:
                url = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url)
                self.q.task_done()
                asyncio.sleep(0.5)
        except asyncio.CancelledError:
            pass

        except Exception as error:
            print(error)

    def add_url(self, url):
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self.q.put_nowait(url)

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
    # URL = 'https://coral.qq.com/article/{}/comment?commentid=0&reqnum=50'
    URL = 'https://coral.qq.com/article/{}/comment?commentid=6257415161087710172&reqnum=50'
    loop = asyncio.get_event_loop()
    crawler = Crawler(url_id='1854269788', max_tasks=5)
    url = URL.format(crawler.url_id)
    crawler.add_url(url)
    loop.run_until_complete(crawler.crawl())
    print('Finished in {:.3f} seconds'.format(crawler.t1 - crawler.t0))
    print(len(crawler.seen_urls))
    crawler.close()
    loop.close()
