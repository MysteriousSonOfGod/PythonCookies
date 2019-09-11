from hashlib import sha224
from time import time

import requests
from lxml import etree
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def questions():
    feed_url = "http://stackoverflow.com/feeds"
    res = requests.get(feed_url).content
    question = etree.HTML(res)
    questions_data = []
    client = MongoClient("localhost", 27017)
    db = client["stack_questions"]
    coll = db["questions"]
    entrys = question.xpath('//entry')
    for entry in entrys:
        author = entry.xpath('author/name/text()')[0]
        link = entry.xpath('author/uri/text()')[0]
        title = entry.xpath('title/text()')[0]
        entry = {
            "_id": sha224(link.encode()).hexdigest(),
            "author": author,
            "link": link,
            "title": title,
            "fetched": int(time())
        }
        print(entry)
        try:
            coll.insert(entry)
        except DuplicateKeyError:
            break
    return questions_data


if __name__ == '__main__':
    questions()
