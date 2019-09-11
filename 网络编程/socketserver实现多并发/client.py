#!/usr/bin/env python3
# coding=utf8

import socket

HOST = '127.0.0.1'
PORT = 8000

client = socket.socket()
client.connect((HOST, PORT))

rec = str(client.recv(1024), encoding='utf8')
print(rec)

while 1:
    comment = input('客户端发起的请求--->\n\n')
    if comment == 'q':
        client.sendall(bytes(comment, encoding='utf8'))
        break
    else:
        client.sendall(bytes(comment, encoding='utf8'))
        print('等待服务器的响应--->\n\n')
        rec = str(client.recv(1024), encoding='utf8')
        print(rec)

client.close()
