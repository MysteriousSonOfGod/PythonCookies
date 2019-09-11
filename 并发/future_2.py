import queue
import threading
import time

import requests
from faker import Factory
from lxml import etree

start = time.time()
fake = Factory.create()


class Meizhi(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    @staticmethod
    def fetch(url):
        headers = {'User-Agent': fake.user_agent()}
        rs = requests.get(url, headers=headers, timeout=2)
        if rs.status_code == 200:
            return rs.content

    def run(self):
        while 1:
            with self.num:
                url = self.queue.get()
                content = self.fetch(url)
                sel = etree.HTML(content)
                urls = sel.xpath('//a[@class="view_img_link"]/@href')
                for url in urls:
                    try:
                        self.download('http:' + url)
                    except Exception as error:
                        print(error)
                self.queue.task_done()
                if self.queue.empty():
                    break

    def download(self, url):
        img = self.fetch(url)
        name = url.split(r'/')[-1]
        print(name)
        with open(name, 'wb') as f:
            f.write(img)


if __name__ == '__main__':
    threads = []
    queue = queue.Queue()
    num = threading.Semaphore(4)
    URL = 'http://jandan.net/ooxx/page-{}#comments'
    meizhi = Meizhi(queue, num)
    for num in range(2407, 2410):
        queue.put(URL.format(num))
    meizhi.start()
    queue.join()

print(time.time() - start)
# 36.42306613922119
