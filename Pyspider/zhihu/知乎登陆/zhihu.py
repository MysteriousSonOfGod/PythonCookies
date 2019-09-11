import requests
from faker import Factory
from lxml import etree

fake = Factory.create()


def login(id, password):
    headers = {'User-Agent': fake.user_agent()}
    url = 'https://www.zhihu.com/login/phone_num'
    data = {
        'phone_num': id,
        'password': password,
    }

    html = requests.get(url, headers=headers).text
    sel = etree.HTML(html)
    if ' name="_xsrf"' in html:
        data['_xsrf'] = sel.xpath('//input[@name="_xsrf"]/@value')[0]

    captcha_url = 'https://www.zhihu.com/captcha.gif?r=1484727248272&type=login'
    captcha = input('请手动输入验证码，网址为' + captcha_url + '\n')
    data['captcha'] = captcha

    session = requests.Session()
    session.post(url, data=data, headers=headers)
    return session


if __name__ == '__main__':
    url = 'https://www.zhihu.com#signin'
    session = login('18520279765', '742369wo')
    text = session.get(url).content
    print(text)
    sel = etree.HTML(text)
    print(sel.xpath('//span[@class="name"]/text()'))
    print('登陆成功')
