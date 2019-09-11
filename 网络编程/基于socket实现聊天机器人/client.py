import socket

client = socket.socket()
client.connect(('127.0.0.1', 8000))
rec = client.recv(1024)
rec = str(rec, encoding='utf8')
print(rec)

while 1:
    comment = input('请客户端输入请求: ')
    if comment == 'q':
        client.sendall(bytes(comment, encoding='utf8'))
        break
    else:
        client.sendall(bytes(comment, encoding='utf8'))
        print('等待服务器响应: ', end="")
        rec = client.recv(1024)
        rec = str(rec, encoding='utf8')
        print(rec)

client.close()
