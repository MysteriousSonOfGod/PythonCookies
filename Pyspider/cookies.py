# from selenium import webdriver
#
#
# browser = webdriver.Chrome()
# browser.get('http://gz.lianjia.com/zufang/GZ0002256850.html')
# cookies = browser.get_cookies()
# print(cookies)
# """
# [{'domain': '.lianjia.com', 'expiry': 1490535381, 'httpOnly': False, 'name': '_jzqb', 'path': '/', 'secure': False, 'value': '1.1.10.1490533581.1'}, {'domain': '.lianjia.com', 'expiry': 1490619980.480026, 'httpOnly': False, 'name': 'select_city', 'path': '/', 'secure': False, 'value': '440100'}, {'domain': 'gz.lianjia.com', 'expiry': 1506258381, 'httpOnly': False, 'name': 'CNZZDATA1255604082', 'path': '/', 'secure': False, 'value': '1909365618-1490530941-%7C1490530941'}, {'domain': 'gz.lianjia.com', 'httpOnly': False, 'name': 'all-lj', 'path': '/', 'secure': False, 'value': '0a26bbdedef5bd9e71c728e50ba283a3'}, {'domain': '.lianjia.com', 'expiry': 1552741580, 'httpOnly': False, 'name': '_smt_uid', 'path': '/', 'secure': False, 'value': '58d7bccc.eec0dc4'}, {'domain': '.lianjia.com', 'expiry': 1805893580.480113, 'httpOnly': False, 'name': 'lianjia_uuid', 'path': '/', 'secure': False, 'value': '46bd52b1-ede0-40b6-839f-1c663716a89b'}, {'domain': '.lianjia.com', 'expiry': 1506258381, 'httpOnly': False, 'name': 'UM_distinctid', 'path': '/', 'secure': False, 'value': '15b0ab980caf8e-084f98713b9b03-3c365601-140000-15b0ab980cb78d'}, {'domain': 'gz.lianjia.com', 'expiry': 1506258381, 'httpOnly': False, 'name': 'CNZZDATA1255849599', 'path': '/', 'secure': False, 'value': '867524947-1490529150-%7C1490529150'}, {'domain': 'gz.lianjia.com', 'expiry': 1506258381, 'httpOnly': False, 'name': 'CNZZDATA1254525948', 'path': '/', 'secure': False, 'value': '1577183356-1490532360-%7C1490532360'}, {'domain': 'gz.lianjia.com', 'expiry': 1506258381, 'httpOnly': False, 'name': 'CNZZDATA1255633284', 'path': '/', 'secure': False, 'value': '440877837-1490532108-%7C1490532108'}, {'domain': '.lianjia.com', 'expiry': 1553605581, 'httpOnly': False, 'name': '_jzqa', 'path': '/', 'secure': False, 'value': '1.2754165206254779000.1490533581.1490533581.1490533581.1'}, {'domain': '.lianjia.com', 'httpOnly': False, 'name': '_jzqc', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.lianjia.com', 'expiry': 1490619981, 'httpOnly': False, 'name': '_jzqckmp', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'gz.lianjia.com', 'expiry': 1553605581, 'httpOnly': False, 'name': '_qzja', 'path': '/', 'secure': False, 'value': '1.1109079271.1490533581190.1490533581190.1490533581190.1490533581190.1490533581190.0.0.0.1.1'}, {'domain': 'gz.lianjia.com', 'expiry': 1490535381, 'httpOnly': False, 'name': '_qzjb', 'path': '/', 'secure': False, 'value': '1.1490533581190.1.0.0.0'}, {'domain': 'gz.lianjia.com', 'httpOnly': False, 'name': '_qzjc', 'path': '/', 'secure': False, 'value': '1'}, {'domain': 'gz.lianjia.com', 'expiry': 1490544000, 'httpOnly': False, 'name': '_qzjto', 'path': '/', 'secure': False, 'value': '1.1.0'}, {'domain': '.mediav.com', 'expiry': 4097260297.649866, 'httpOnly': False, 'name': 'huid', 'path': '/', 'secure': False, 'value': '70aa20896fb715cd4d01276a05013c5e'}, {'domain': '.lianjia.com', 'expiry': 1490535381.544645, 'httpOnly': False, 'name': 'lianjia_ssid', 'path': '/', 'secure': False, 'value': '3d9a5440-3a26-4eae-afd1-d0f8713b1b28'}, {'domain': '.mediav.com', 'expiry': 1493154381.236443, 'httpOnly': False, 'name': 'ckmts', 'path': '/', 'secure': False, 'value': 'PUP-wH_j,P6P-wH_j,-GP-wH_j,RGP-wH_j,L6N-wH_j,J6P-wH_j,bUP-wH_j'}, {'domain': '.mediav.com', 'expiry': 4097260297.42229, 'httpOnly': False, 'name': 'v', 'path': '/', 'secure': False, 'value': '^.36S]iNXz:#s[D!u)tG'}]
# """
# browser.close()


import requests

print(requests.get('http://zh.lianjia.com/zufang/pg97/', allow_redirects=False, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 54.0.2840.99Safari /537.36'}).status_code)
session = requests.Session()
session.get('http://zh.lianjia.com/zufang/pg97/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 54.0.2840.99Safari /537.36'})
print(session.cookies.get_dict())
# """
# {'lianjia_ssid': 'e409b1ef-dfd1-4384-9dcc-c6763271f17b', 'lianjia_uuid': '7b4cb41b-3bdf-49b4-9281-02bd90709884', 'select_city': '440100', 'all-lj': '80b391239fd880f59f779618fca39507'}
# """
#
#
# import aiohttp
# import asyncio
#
# async def fetch(session, url):
#     async with session.get(url) as response:
#         print(response.status)
#         cookies = response.cookies.copy()
#         print(cookies)
#
#         return await response.text()
#
# async def main(loop):
#     async with aiohttp.ClientSession(loop=loop,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 54.0.2840.99Safari /537.36'}) as session:
#         await fetch(session, 'http://gz.lianjia.com/')
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))
# loop.close()
