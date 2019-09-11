from lxml import etree
from selenium import webdriver

url = 'http://music.163.com/#/song?id=32922450'

browser = webdriver.PhantomJS()

browser.get(url)
# browser.switch_to.frame(browser.find_element_by_xpath('//iframe'))
browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
# 从frame回到主文档
# browser.switch_to.default_content()
source = browser.page_source
browser.close()
selector = etree.HTML(source)
lyric1 = selector.xpath('//div[@id="lyric-content"]/text()')
lyric2 = selector.xpath('//div[@id="lyric-content"]/div[@id="flag_more"]/text()')
lyrics = lyric1 + lyric2
for lyric in lyrics:
    print(lyric)
