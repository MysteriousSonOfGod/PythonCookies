# coding=utf8


import os
import queue
import select
import socket

# 创建 socket 套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

# 配置参数

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('127.0.0.1', 8080)
server.bind(server_address)
server.listen(10)
inputs = [server]
outputs = []
message_queue = {}

while inputs:
    print('waiting for next event')
    # readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    # 最后一个是超时，当前连接要是超过这个时间的话，就会kill
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)

    if not (readable or writeable or exceptional):
        print('Time Out')
        break
    for s in readable:
        if s in server:
            connection, client_address = s.accept()
            print('connection from ', client_address)
            connection.setblocking(0)
            inputs.append(connection)
            message_queue[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print('received', data, 'from', s.getpeername())
                message_queue[s].put(data)

                if s not in outputs:
                    outputs.append(s)
            else:
                print('closing, ', client_address)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                # 清除队列信息
                del message_queue[s]
    for s in writeable:
        try:
            next_msg = message_queue[s].get_nowait()
        except queue.Empty:
            print(' ', s.getpeername(), 'queue empty')
            outputs.remove(s)
        else:
            print('sending ', next_msg, 'to', s.getpeername())
            os.popen('sleep 5').read()
            s.send(next_msg)

    for s in exceptional:
        print('exception condition on ', s.getpeername())
        # stop listening for input on the connection
        inputs.remove(s)

        if s in outputs:
            outputs.remove(s)
        s.close()

        # 清除队列信息
        del message_queue[s]
