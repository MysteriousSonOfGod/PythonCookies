#!/usr/bin/env python3


import socket

obj = socket.socket()
obj.connect(('127.0.0.1', 6254))

obj.close()
