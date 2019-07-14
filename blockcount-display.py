#!/usr/bin/env python3

import RPi.GPIO as GPIO
import Pi7SegPy as Pi7Seg # https://pypi.org/project/Pi7SegPy/
from threading import Thread
import time
import bitcoin.rpc

Pi7Seg.init(18,23,24,2,4) # Initialize with Data:GPIO17, Clock:GPIO27, Latch:GPIO22, with 2 shift registers and 4 7 segment displays on each register

def display():
    global a
    while True:
        #time.sleep(0.1) # not working attempt to reduce 100% cpu usage
        b = list(a)
        for k in range(0, 8-len(b)):
            b = [" "] + b
        order = [3,2,1,0,7,6,5,4]
        out = [" "]*8
        for i in range(0, 8):
            c = b[order[i]]
            if c.isnumeric():
                out[i] = int(c)
        Pi7Seg.show(list(out))
    GPIO.cleanup # https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi

def counter():
    global a
    while True:
        try:
            proxy = bitcoin.rpc.Proxy()
            x = str(proxy.getblockcount())
        except:
            x = a
        if x != a:
            for l in range(0, 10):
                a = "        "
                time.sleep(0.25)
                a = x
                time.sleep(0.25)
        time.sleep(60)

def main():
    global a
    a = "        "

    display_thread = Thread(target=display)
    display_thread.start()

    counter_thread = Thread(target=counter)
    counter_thread.start()

if __name__ == '__main__':
    main()
