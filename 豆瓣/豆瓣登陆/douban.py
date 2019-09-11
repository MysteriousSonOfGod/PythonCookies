import requests
from faker import Factory
from lxml import etree

fake = Factory.create()


def login(id, password):
    headers = {'User-Agent': fake.user_agent()}
    url = 'https://accounts.douban.com/login'
    data = {'source': 'None',
            'redir': 'https://www.douban.com',
            'form_email': id,
            'form_password': password,
            'remember': 'on',
            'login': '登录'
            }

    html = requests.get(url, headers=headers).text
    sel = etree.HTML(html)
    if 'name="ck"' in html:
        data['ck'] = sel.xpath('//input[@name="ck"]/@value')[0]

    captcha_image = sel.xpath('//img[@id="captcha_image"]/@src')
    if captcha_image:
        captcha_image = captcha_image[0]
        captcha_id = sel.xpath('//input[@name="captcha-id"]/@value')[0]
        captcha_solution = input('请手动输入验证码，网址为' + captcha_image + '\n')
        data['captcha-solution'] = captcha_solution
        data['captcha-id'] = captcha_id

    session = requests.Session()

    res = session.post(url, data=data, headers=headers).text

    assert 'xnotes' in res

    return session


if __name__ == '__main__':
    url = 'https://www.douban.com/'

    session = login('603269622@qq.com', '742369wo')

    text = session.get(url).content
    sel = etree.HTML(text)
    print(sel.xpath('//span/text()'))
    print('登陆成功')
