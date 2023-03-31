import time

import machine

temp1 = machine.ADC(machine.Pin(25))  # , atten=machine.ADC.ATTN_11DB)
temp1.atten(machine.ADC.ATTN_11DB)

temp2 = machine.ADC(machine.Pin(26))  # , atten=machine.ADC.ATTN_11DB)
temp2.atten(machine.ADC.ATTN_11DB)

from client_funcs import request, find_server


import network

wlan_sta = network.WLAN(network.STA_IF)

def connect():
    wlan_sta.active(False)
    wlan_sta.active(True)
    #wlan_sta.connect("ZTE Blade L2", "&&&&&&&&")
    wlan_sta.connect("smartpark_service", "smartpark_2021")

    while not wlan_sta.isconnected():
        print('Connecting...')
        time.sleep(1)
connect()


serv_ip = find_server()
print(serv_ip)


def c_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    wlan_sta.active(False)

    inside = c_map(temp1.read(), 0, 4095, 0, 3300) / 10 - 273
    outside = c_map(temp2.read(), 0, 4095, 0, 3300) / 10 - 273
    print(inside, outside)
    connect()
    request({'event': 'set temp', 'inside': inside, 'outside': outside}, serv_ip, 65432)
    time.sleep(1)


