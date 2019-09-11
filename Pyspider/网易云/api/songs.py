import base64
import codecs
import csv
import sys
import time
from multiprocessing.dummy import Pool

import requests
import ujson
from Crypto.Cipher import AES
from faker import Factory

start = time.time()
fake = Factory.create()
file = 'comments.csv'

headers = {'User-Agent': fake.user_agent(),
           'Cookie': 'appver=1.5.0.75771;',
           'Referer': 'http://music.163.com/'
           }


def create_csv():
    with open(file, 'w', ) as csvfile:
        fieldnames = ['用户', '评论', '时间']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def write_to_csv(house_dict):
    with open(file, 'a+', encoding='utf8') as csvfile:
        fieldnames = ['用户', '评论', '时间']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(house_dict)


# limitMax = 100
# limit = 100

pubKey = "010001"
modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
nonce = "0CoJUm6Qyw8W8jud"


def aesEncrypt(text, seckey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(seckey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    ciphertext = ciphertext.decode()
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    text = text.encode()
    rs = int(codecs.encode(text, 'hex').decode(), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def fetchNum(url, musicID):
    api = {'rid': 'R_SO_4_' + musicID, 'offset': '0', 'total': 'true', 'limit': '20', 'csrf_token': ''}
    _api = ujson.dumps(api)
    encText = aesEncrypt(aesEncrypt(_api, nonce), 16 * 'F')
    encSecKey = rsaEncrypt(16 * 'F', pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    req = requests.post(url, headers=headers, data=data).json()
    total = req['total']
    return total


def fetch(url, musicID, num):
    global count
    api = {'rid': 'R_SO_4_' + musicID, 'offset': num, 'total': 'true', 'limit': '100', 'csrf_token': ''}
    _api = ujson.dumps(api)
    encText = aesEncrypt(aesEncrypt(_api, nonce), 16 * 'F')
    encSecKey = rsaEncrypt(16 * 'F', pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    req = requests.post(url, headers=headers, data=data)
    if req.status_code == 200:
        req = req.json()
        try:
            for item in req['comments']:
                comments = dict()
                count += 1
                comments['用户'] = item['commentId']
                comments['评论'] = item['content']
                timeNow = int(str(item['time'])[0: -3])
                timeLocal = time.localtime(timeNow)
                comments['时间'] = time.strftime("%Y-%m-%d %H:%M:%S", timeLocal)
                write_to_csv(comments)
                print(item['content'])
        except Exception as error:
            print(error)
    else:
        print(req.status_code)


if __name__ == '__main__':
    _id = sys.argv[1]
    create_csv()
    pool = Pool(20)
    count = 0
    url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}/?csrf_token="
    musicURL = url.format(_id)
    total = fetchNum(musicURL, _id)
    nums = int(total / 100) + 2
    args = []
    for num in range(1, nums):
        args.append((musicURL, _id, str((num - 1) * 100)))
    pool.starmap_async(fetch, args)
    pool.close()
    pool.join()
    print(count)

end = time.time()
print(end - start)
