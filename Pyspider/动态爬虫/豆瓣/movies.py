from selenium import webdriver

URI = 'https://movie.豆瓣.com/'

browser = webdriver.Chrome()
browser.get(URI)
while 1:
    try:
        browser.find_element_by_xpath('//a[@class="more"]').click()
    except Exception as e:
        print(e)
