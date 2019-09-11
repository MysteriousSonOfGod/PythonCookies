#!/usr/bin/env python3
# coding=utf8


import os
import socket

client = socket.socket()
client.connect(('127.0.0.1', 5000))

name = input('请输入要上传的文件--->\n')
size = os.path.getsize(name)
client.sendall(bytes(str(size), encoding='utf8'))
file_size = client.recv(1024)
print('文件大小为 ', size, '服务端返回的文件大小为 ', file_size)

with open(name, 'rb') as f:
    for line in f.readlines():
        client.sendall(line)

client.close()
