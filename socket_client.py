import socket

HOST = 'localhost'
PORT = 9999


def conn_one():
    s = socket.socket()
    s.connect((HOST, PORT))
    while True:
        msg = input('>>:').strip()
        s.send(msg.encode('utf-8'))
        # s.send(('hello ').encode('utf-8'))
        data = s.recv(1024)
        print('recved:', data.decode())
    s.close()


conn_one()
