import chardet
import requests
from faker import Factory

fake = Factory.create()


def encode(url):
    rs = requests.get(url, headers={'User-Agent': fake.user_agent()})
    if rs.status_code == 200:
        encode_code = chardet.detect(rs.content)['encoding']
        return encode_code


if __name__ == '__main__':
    code = encode('https://www.zhihu.com/question/21471960')
    print(code)
