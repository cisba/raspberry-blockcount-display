#!/usr/bin/env python3
'''
Simple daemon to print a string on two row of four "7 segment" display
'''
# GPIO.cleanup # https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi pylint: disable=C0301

import time
from threading import Thread
import urllib.request
import logging

# pip install RPi.GPIO Pi7SegPy python-bitcoinlib python-daemon
import Pi7SegPy as Pi7Seg # https://pypi.org/project/Pi7SegPy/
import bitcoin.rpc
import daemon

# Initialize with Data:GPIO17, Clock:GPIO27, Latch:GPIO22,
# with 2 shift registers and 4 7 segment displays on each register
Pi7Seg.init(18, 23, 24, 2, 4)

data = "        " # pylint: disable=C0103

def display():
    ''' show the string on the display'''

    global data # pylint: disable=W0603,C0103
    while True:
        b_l = list(data)
        for _ in range(0, 8-len(b_l)):
            b_l = [" "] + b_l
        order = [3, 2, 1, 0, 7, 6, 5, 4]
        out = [" "]*8
        for index in range(0, 8):
            char = b_l[order[index]]
            if char.isnumeric():
                out[index] = int(char)
        Pi7Seg.show(list(out))



def counter():
    ''' set value to be printed on the diplay'''

    logfile = "/var/log/bitcoin/blockcount-display.log"
    log_fmt = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(filename=logfile, format=log_fmt, level=logging.DEBUG)
    logging.info("Start")
    logging.debug("Started in DEBUG mode")

    global data # pylint: disable=W0603,C0103
    blck = "        "
    prev_blck = ""
    while True:

        # blockchain
        try:
            proxy = bitcoin.rpc.Proxy()
            blck = str(proxy.getblockcount())
            # with open('/var/log/bitcoin/getblockcount', 'r') as f_h:
            #    blck = str(int(f_h.read()))
        except Exception as err: # pylint: disable=W0703
            logging.error(str(err))

        if blck != prev_blck:
            for _ in range(0, 10):
                data = "        "
                time.sleep(0.25)
                data = blck
                time.sleep(0.25)
            prev_blck = blck
        data = blck
        logging.debug("block %s" % data) # pylint: disable=W1201
        time.sleep(9)

        # block gap
        if blck.isnumeric():
            try:
                url = "https://blockchain.info/q/getblockcount"
                last = int(urllib.request.urlopen(url).read())
                data = str(int(blck) - last)
            except Exception as err: # pylint: disable=W0703
                logging.error(str(err))
            logging.debug("gap %s" % data) # pylint: disable=W1201
            time.sleep(3)

        # temperature
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f_h:
                data = str(int(float(f_h.read())/1000))
        except Exception as err: # pylint: disable=W0703
            logging.error(str(err))
        logging.debug("temperature %s" % data) # pylint: disable=W1201
        time.sleep(3)

    logging.info("End")


def main():
    ''' main function '''

    with daemon.DaemonContext():

        display_thread = Thread(target=display)
        display_thread.start()

        counter_thread = Thread(target=counter)
        counter_thread.start()


if __name__ == '__main__':
    main()
