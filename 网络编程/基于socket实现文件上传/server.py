#!/usr/bin/env python3
# coding=utf8


import socket

sk = socket.socket()
sk.bind(('127.0.0.1', 5000))
sk.listen(5)

while 1:
    conn, address = sk.accept()
    file_size = str(conn.recv(1024), encoding='utf8')
    conn.sendall(bytes(file_size, encoding='utf8'))
    total_size = int(file_size)
    has_rec = 0

    with open('备份.jpg', 'wb') as f:
        while 1:
            if total_size == has_rec:
                break
            data = conn.recv(1024)
            f.write(data)
            has_rec += len(data)
