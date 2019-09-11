# coding: utf-8

from itertools import count


def pro():
    print('先运行这里--->')
    for num in count():
        num = yield num
        if num == -1:
            break


def con(p):
    num = p.send(None)
    num += 1
    while True:
        try:
            num = num + 2 if num != 9 else -1
            p.send(num)
            print(num, end='--->\n')
        except StopIteration:
            break


p = pro()
con(p)
