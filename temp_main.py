import time
import socket
import machine

temp = machine.ADC(machine.Pin(15))


while True:
    print(temp.read())
    time.sleep(1)


