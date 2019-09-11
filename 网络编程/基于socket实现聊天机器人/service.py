import socket

sk = socket.socket()
sk.bind(('127.0.0.1', 8000))
sk.listen(5)

while 1:
    conn, address = sk.accept()
    conn.sendall(bytes('欢迎你\n', encoding='utf8'))

    while 1:
        print('等待客户端的请求: ', end="")
        rec = conn.recv(1024)
        rec = str(rec, encoding='utf-8')
        print(rec)
        if rec == 'q':
            break

        answer = input('请服务器给出响应: ')
        conn.sendall(bytes(answer, encoding='utf8'))
