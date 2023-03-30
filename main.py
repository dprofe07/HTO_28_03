import time
import machine

from client_funcs import request, find_server

serv_ip = find_server()

temp1 = machine.ADC(machine.Pin(25))
temp1.atten(machine.ADC.ATTN_11DB)

temp2 = machine.ADC(machine.Pin(26))
temp2.atten(machine.ADC.ATTN_11DB)


def c_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    inside = c_map(temp1.read(), 0, 4095, 0, 3300) / 10 - 273
    outside = c_map(temp2.read(), 0, 4095, 0, 3300) / 10 - 273

    request({'event': 'set temp', 'inside': inside, 'outside': outside}, serv_ip, 65432)

    time.sleep(1)


