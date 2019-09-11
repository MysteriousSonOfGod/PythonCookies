import time

from selenium import webdriver

url = 'http://item.jd.com/10296643495.html'


def fetch(url):
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)
    html = browser.execute_script('return document.documentElement.outerHTML')
