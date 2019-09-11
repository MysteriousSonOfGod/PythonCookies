import os
import time

import requests
from faker import Factory
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

URI = 'http://www.tazhe.com/mh/27326/'
fake = Factory.create()


class Hunshou(object):
    def __init__(self, URI, path, broswer):
        self.URI = URI
        self.path = os.path.join(os.path.abspath('.'), path)
        self.broswer = broswer

    def response(self, url):
        print(url)
        headers = {'User-Agent': fake.user_agent()}
        rs = requests.get(url, headers=headers)
        return rs.content

    def download(self, image, dirs, name):
        paths = os.path.join(self.path, dirs)
        if os.path.exists(paths):
            pass
        else:
            os.makedirs(paths)
        paths = os.path.join(paths, name)
        if os.path.isfile(paths):
            pass
        else:
            with open(paths, 'wb') as img:
                img.write(self.response(image))

    def chapters(self):
        self.broswer.get(self.URI)
        urls = self.broswer.find_elements_by_xpath('//div[@id="play_0"]/ul/li/a')
        urls = [url.get_attribute('href') + '?p={}' for url in urls]
        urls.reverse()
        chaps = self.broswer.find_elements_by_xpath('//div[@id="play_0"]/ul/li/a')
        chaps = [chapter.text for chapter in chaps]
        chaps.reverse()
        return (urls, chaps)

    def section(self):
        urls, dirs = self.chapters()
        for url, name in zip(urls, dirs):
            num = 1
            while 1:
                self.broswer.get(url.format(num))
                images = self.broswer.find_elements_by_xpath('//div[@class="tbCenter"]/img')[0].get_attribute('src')
                imgdir = self.broswer.find_element_by_xpath('//h1/span').text
                self.download(images, name, imgdir + '.jpg')
                self.broswer.find_element_by_xpath('//a[@class="next"]').click()
                try:
                    self.broswer.find_element_by_xpath('//div[@id="msgDiv"]')
                    break
                except NoSuchElementException:
                    num += 1
                except Exception as e:
                    print(e)

    def run(self):
        self.section()
        self.broswer.close()


if __name__ == '__main__':
    start = time.time()
    hunshou = Hunshou('http://www.tazhe.com/mh/27326/', '魂收', webdriver.Chrome())
    hunshou.run()
    end = time.time()
    print(end - start)
