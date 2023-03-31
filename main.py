import time

import machine
import network
import json
import socket
import time

from client_funcs import find_server


serv = machine.PWM(machine.Pin(27), freq=50)
fan = machine.Pin(26, machine.Pin.OUT)


wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(False)
wlan_sta.active(True)
wlan_sta.connect("smartpark_service", "smartpark_2021")
#wlan_sta.connect("LEGION-WIFI", "&&&&&&&&")
while not wlan_sta.isconnected():
    print('Connecting...')
    time.sleep(1)
print(wlan_sta.status())


class Client:
    def __init__(self):
        self.do_loop = True

        self.serv_ip = find_server(True)
        print(self.serv_ip)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', 65431))

    def kill(self):
        self.do_loop = False

    def loop(self):
        while self.do_loop:
            self.sock.listen()
            conn, addr = self.sock.accept()

            res = ''

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                elif data.endswith(b"\1"):
                    data = data[:-1]
                    res += data.decode("utf-8")
                    break
                res += data.decode("utf-8")
            print(res)
            conn.send(json.dumps({'event': 'response'}).encode("utf-8"))
            json_res = json.loads(res)
            if json_res['fan'] == 'on':
                fan.on()
            else:
                fan.off()

            if json_res['window'] == 'open':
                serv.duty(115)
            else:
                serv.duty(40)
            time.sleep(0.1)
            conn.close()


cl = Client()
cl.loop()


