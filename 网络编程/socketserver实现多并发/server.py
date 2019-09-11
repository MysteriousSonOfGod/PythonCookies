#!/usr/bin/env python3
# coding=utf8

import socketserver


class ChatServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall(bytes('你好，欢迎登陆', encoding='utf8'))

        while 1:
            print('等待客户端请求--->\n\n')
            rec = str(conn.recv(1024), encoding='utf8')
            print(rec)

            if rec == 'q':
                break
            comment = input('服务器给出的响应--->\n\n')
            conn.sendall(bytes(comment, encoding='utf8'))


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8000
    server = socketserver.ThreadingTCPServer((HOST, PORT), ChatServer)
    server.serve_forever()
