import socket
import threading
import time
import json

from client_funcs import request


class Server:
    def __init__(self, host, port, uuid):
        self.do_loop = True
        self.do_mainloop = True
        self.inside_temp = 20.0
        self.outside_temp = 8.0
        self.uuid = uuid
        self.port = port
        self.host = host
        self.move_client_ip = None
        self.handlers = {}

        self.register_handler('get uuid', self.get_uuid)
        self.register_handler('set temp', self.set_temp)
        self.register_handler('get temp', self.get_temp)

        self.sock_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_broadcast.bind((host, port))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

        threading.Thread(target=self.loop_tcp).start()
        threading.Thread(target=self.loop_broadcast).start()

    def kill(self):
        self.do_loop = False

    def register_handler(self, event, handler):
        self.handlers[event] = handler

    def send(self, data, conn):
        text = json.dumps(data) + '\1'
        print('SENDING: %s' % text)
        conn.send(text.encode('utf-8'))

    def loop_broadcast(self):

        while self.do_loop:
            text, addr = self.sock_broadcast.recvfrom(1024)
            got_data = json.loads(text.decode('utf-8'))
            if got_data['event'] == 'finding_server':
                print('FINDING SERVER')
                if got_data['moving']:
                    self.move_client_ip = addr[0]
                    print('FOUND MOVE CLIENT 1')
                    self.do_mainloop = False
                    time.sleep(2)
                    self.do_mainloop = True
                    threading.Thread(target=self.loop_main).start()
                data = json.dumps({
                    'role': 'server',
                })
                self.sock_broadcast.sendto(data.encode('utf-8'), addr)

    def loop_tcp(self):
        print('Ready')
        while self.do_loop:
            time.sleep(0.1)
            self.sock.listen()
            conn, addr = self.sock.accept()

            with conn:
                print(f"Connected by {addr}")
                res = ""
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    elif data.endswith(b"\1"):
                        data = data[:-1]
                        res += data.decode("utf-8")
                        break
                    res += data.decode("utf-8")
                print(f'GOT: {res}')
                json_res = json.loads(res)
                if json_res['event'] in self.handlers:
                    self.handlers[json_res['event']](conn, addr, json_res)
                else:
                    print('GOT UNKNOWN MESSAGE')

    def loop_main(self):
        while self.move_client_ip is None:
            time.sleep(1)
        print('FOUND MOVE CLIENT 2')
        while self.do_mainloop:
            time.sleep(1)
            print(f'LOOP, {self.inside_temp=}, {self.outside_temp=}')

            if 18 <= self.inside_temp <= 24:
                print('GOOD')
                request({'window': 'close', 'fan': 'off'}, self.move_client_ip, 65431)
                # todo выключить вентилятор
            else:
                if self.inside_temp < 18 < self.outside_temp:
                    request({'window': 'open', 'fan': 'off'}, self.move_client_ip, 65431)
                    # todo открыть форточку
                    # todo выключить вентилятор
                    pass
                elif self.inside_temp > 24 > self.outside_temp:
                    request({'window': 'open', 'fan': 'on'}, self.move_client_ip, 65431)
                    # todo закрыть форточку
                    # todo включить вентилятор
                    pass
                else:
                    print('BAD')
                    request({'window': 'close', 'fan': 'off'}, self.move_client_ip, 65431)

    def get_uuid(self, conn, addr, data):
        print('MY UUID IS ' + str(self.uuid))
        self.send({'uuid': self.uuid, 'event': 'response'}, conn)

    def set_temp(self, conn, addr, data):
        self.inside_temp = data.get('inside', self.inside_temp)
        self.outside_temp = data.get('outside', self.outside_temp)
        self.send({'good': 'ok', 'event': 'response'}, conn)

    def get_temp(self, conn, addr, data):
        conn.send(bytes(str({'event': 'response', 'inside': self.inside_temp, 'outside': self.outside_temp}), 'utf-8'))


server = Server('', 65432, 10005789)