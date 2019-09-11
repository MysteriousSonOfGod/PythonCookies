import base64
import codecs

import requests
import ujson
from Crypto.Cipher import AES
from faker import Factory

fake = Factory.create()

headers = {'User-Agent': fake.user_agent(),
           'Cookie': 'appver=1.5.0.75771;',
           'Referer': 'http://music.163.com/'
           }

api = {'rid': 'R_SO_4_186016', 'offset': '0', 'total': 'true', 'limit': '20', 'csrf_token': ''}
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


url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_186016/?csrf_token="

if __name__ == '__main__':
    _api = ujson.dumps(api)
    encText = aesEncrypt(aesEncrypt(_api, nonce), 16 * 'F')
    encSecKey = rsaEncrypt(16 * 'F', pubKey, modulus)

    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    req = requests.post(url, headers=headers, data=data).json()
    count = 0
    for item in req['comments']:
        count += 1
        print(item['content'])

    print(count)
