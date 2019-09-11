import requests
from faker import Factory

fake = Factory.create()

url = 'http://music.163.com/weapi/song/lyric?csrf_token='

data = {
    'params': 'iuGCIrdE4PXlnPnsU5HaRM8qEMB1etrHzSAA4423QHPml2dj3KeRaqS3KRW0kRid3gNC8KkkIDcrVVJERlkVPg1yz7f6Vk+JsRpn53wYb8I=',
    'encSecKey': '35186b34fe9df146351fbfdfc26cbc1a5c19b9f36fc1994a163e13395f09994e99d870a16fb0fcf351b1ac48734606a42fed7eb82034c455046ef5ad07687584741893300a304182f9a3c0f211d7356b7c457172c8f268829ea8ab169e29d784b586a637144359f0395217f994dd0e724b94919c365e6fbd804e0b6ee04aa6a6'}

rs = requests.post(url, headers={'User-Agent': fake.user_agent(),
                                 'Origin': 'http://music.163.com',
                                 'Referer': 'ttp://music.163.com/song?id=186016'},
                   data=data).json()

lyrics = rs['lrc']['lyric']
print(lyrics)
