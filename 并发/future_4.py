import time
from concurrent.futures import ProcessPoolExecutor

import requests
from faker import Factory
from lxml import etree

fake = Factory.create()


def fetch(url):
    headers = {'User-Agent': fake.user_agent()}
    rs = requests.get(url, headers=headers)
    if rs.status_code == 200:
        return rs.content


def download(url):
    img = fetch(url)
    name = url.split(r'/')[-1]
    print(name)
    with open(name, 'wb') as f:
        f.write(img)


def main(url):
    content = fetch(url)
    sel = etree.HTML(content)
    urls = sel.xpath('//a[@class="view_img_link"]/@href')
    for url in urls:
        download('http:' + url)


if __name__ == '__main__':
    start = time.time()
    URL = 'http://jandan.net/ooxx/page-{}#comments'
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(main, [URL.format(num) for num in range(2407, 2410)])
    print(time.time() - start)

# 19.65689253807068
