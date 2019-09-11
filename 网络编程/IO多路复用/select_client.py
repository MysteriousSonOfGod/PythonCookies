# coding=utf8

import socket

host = '127.0.0.1'
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(b'coming from select client')
s.close()
