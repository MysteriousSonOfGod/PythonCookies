import socket

import requests
import socks

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket

_ip = requests.get('http://icanhazip.com/')
print(_ip)
