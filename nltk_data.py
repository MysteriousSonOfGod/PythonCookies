import requests
from lxml import etree

URL = 'http://www.nltk.org/nltk_data/'
rs = requests.get(URL).content
selector = etree.HTML(rs)
packages = selector.xpath('//packages/package/@url')
for package in packages:
    with open('nltk_data.txt', 'a+') as data:
        print(package)
        data.write(package + '\n')
