import time

import machine

serv = machine.PWM(machine.Pin(27), freq=50)
fan = machine.Pin(26, machine.Pin.OUT)

fan.on()
a = 40
while True:
    if a == 40:
        a = 115
    else:
        a = 40
    serv.duty(a)
    time.sleep(1)


