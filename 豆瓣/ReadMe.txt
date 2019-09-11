movie.py为爬取豆瓣的电影，运行方式 python movie.py 日本(日本为参数)

book.py脚本为爬取豆瓣的书籍写入books.csv文件中，其中出现错误，偶尔要考虑没有评分，进行异常处理
string = "Carver's dozen―レイモンド・カーヴァー傑作選"
with open('book.txt','w') as f:
    f.write(string)

出现错误
UnicodeEncodeError: 'gbk' codec can't encode character '\u30fb' in position 20:illegal multibyte sequence

解决办法
with open('book.txt','w',encoding='utf-8') as f:
    f.write(string)

book1.py脚本为book.py的第二版，采用多线程，但是几分钟后被ban了
book2.py为第三版，添加了cookies，但是开启50个线程，程序突然奔溃，原因不知
book3.py第三版，用asyncio,和aiohttp，但是没有完成