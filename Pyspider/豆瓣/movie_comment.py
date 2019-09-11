import argparse
import asyncio
import csv
import re

import aiohttp
from faker import Factory
from lxml import etree

ap = argparse.ArgumentParser()
ap.add_argument('-m', '--movie', required=True,
                help='Input your movies number')
ap.add_argument('-o', '--output', required=True,
                help='Input your output file')
args = vars(ap.parse_args())

fake = Factory.create()


def create_csv():
    file = args['output']
    with open(file, 'w', ) as csvfile:
        fieldnames = ['评论']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


class DoubanComment(object):
    def __init__(self, max_tries=2, max_tasks=4, loop=asyncio.get_event_loop()):
        self.loop = loop
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.q = asyncio.Queue(loop=self.loop)
        self.seen_urls = set()
        self._session = None
        self.file = args['output']

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(headers={'User-Agent': fake.user_agent(),
                                                           'X-Requested-With': 'XMLHttpRequest'},
                                                  loop=self.loop)
        return self._session

    def close(self):
        self.session.close()

    def write_to_csv(self, comments):
        with open(self.file, 'a+', encoding='utf8') as csvfile:
            fieldnames = ['评论']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            comment_dict = dict()
            comment_dict['评论'] = comments
            writer.writerow(comment_dict)

    async def fetch(self, url, sign):
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
                if sign == 'first':
                    await self.comments(response)
                elif sign == 'second':
                    await self.fulls(response)
                elif sign == 'third':
                    await self.reviews(response)
            else:
                print('fail fetched', response.status)
        finally:
            await response.release()

    async def comments(self, response):
        print('抓取评论...')
        try:
            content = await response.text()
            sel = etree.HTML(content)
            review_comments = sel.xpath('//div[@class="short-content"]/text()')
            review_fulls = sel.xpath('//div[@class="short-content"]/a/@href')
            review_tells = re.sub("[' '|'\n'|'\r'|'\t']*", '', content)
            next_page = sel.xpath('//span[@class="next"]/a/@href')
            if next_page:
                self.add_url('https://movie.douban.com/subject/{}/reviews'.format(args['movie']) + next_page[0],
                             'first')

            if review_comments:
                review_comments = [review_comment for review_comment in map(str.strip, review_comments) if
                                   review_comment != '']
                for review_comment in review_comments:
                    self.write_to_csv(review_comment)

            if review_fulls:
                for review_full in review_fulls:
                    self.add_url(review_full, 'second')

            targets = re.findall(
                '<divid="review_(\d+)_short"class="review-short"><divclass="short-content"><pclass="main-title-tip">这篇影评可能有剧透</p>',
                review_tells)
            if targets:
                for target in targets:
                    self.add_url('https://movie.douban.com/j/review/{}/full'.format(target), 'third')
        except Exception as e:
            print(e)

    async def fulls(self, response):
        print('抓取评论...')
        try:
            rs = await response.text()
            sel = etree.HTML(rs)
            comments_1 = sel.xpath('//div[@property="v:description"]/p/text()')
            if comments_1:
                comments = re.sub('["\n"]*', '', comments_1[0])
                self.write_to_csv(comments)
            comments_2 = sel.xpath('//div[@property="v:description"]/text()')
            if comments_2:
                for comment_2 in comments_2:
                    self.write_to_csv(re.sub('["\n"|" "]', '', comment_2))
        except Exception as e:
            print(e)

    async def reviews(self, response):
        try:
            rs = await response.json()
            comments = rs['html']
            comments = re.sub('["<p>|"</p>"]*', '', comments)
            self.write_to_csv(comments)
        except Exception as e:
            print(e)

    async def work(self):
        try:
            while 1:
                url, sign = await self.q.get()
                await self.fetch(url, sign)
                self.q.task_done()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(e)

    def add_url(self, url, sign):
        if url not in self.seen_urls:
            self.seen_urls.add(url)
            self.q.put_nowait((url, sign))

    async def crawl(self):
        workers = [asyncio.Task(self.work(), loop=self.loop)
                   for _ in range(self.max_tasks)]
        await self.q.join()
        for w in workers:
            w.cancel()


if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/{}/reviews'.format(args['movie'])
    create_csv()
    loop = asyncio.get_event_loop()
    crawler = DoubanComment(max_tasks=5)
    crawler.add_url(url, 'first')
    loop.run_until_complete(crawler.crawl())
    crawler.close()
    loop.close()
