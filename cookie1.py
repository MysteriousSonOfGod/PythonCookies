# coding: utf-8

from itertools import count


def pro():
    # 生成从0到无穷
    for num in count(start=1):
        yield con(num)


def con(num):
    if num > 11:
        raise StopIteration
    print(num, end='-->\n')


# # list(pro())
for i in pro():
    i
