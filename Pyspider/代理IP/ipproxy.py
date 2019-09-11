import requests

url = 'http://icanhazip.com/'

proxies = {
    "http": "http://45.32.52.146:8080",
    "https": "http://45.32.52.146:8080",
}


def fetch(url):
    rs = requests.get(url, proxies=proxies).text
    print(rs)


fetch(url)
