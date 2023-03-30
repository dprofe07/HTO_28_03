import json
import socket
import threading
import time

from client.client_funcs import find_server


class Client:
    def __init__(self):
        self.do_loop = True

        self.serv_ip = find_server(True)
        print(self.serv_ip)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 65431))

        threading.Thread(target=self.loop).start()

    def kill(self):
        self.do_loop = False

    def loop(self):
        while self.do_loop:
            self.sock.listen()
            conn, addr = self.sock.accept()
            with conn:
                res = ''

                while True:
                    data = conn.recv(1024)
                    print(data)
                    if not data:
                        break
                    elif data.endswith(b"\1"):
                        data = data[:-1]
                        res += data.decode("utf-8")
                        break
                    res += data.decode("utf-8")
                print(f'GOT: {res}')


cl = Client()
