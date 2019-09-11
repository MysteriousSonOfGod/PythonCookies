#!/usr/bin/env python3


import socket

sk = socket.socket()
sk.bind(('127.0.0.1', 6254))
sk.listen(5)

print('waiting customer connect...')
conn, address = sk.accept()
print('address= ', address, '\n', 'conn= ', conn)
