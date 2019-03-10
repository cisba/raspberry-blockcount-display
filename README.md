# Raspberry blockcount display

This script execute the bitcoinrpc getblockcount() call periodically, obtaining the number of blocks in the longest blockchain. 

Then display it in an [8-Digit LED Tube 7 Segments 74HC595 driven](https://www.amazon.com/gp/product/B07F42B6T4/) connected to the raspberry.

Every new block [flash](https://youtu.be/ye30J9S7PQI) the number.

## Pinout

| 74HC595     | GPIO |
|------------:|:-----|
| +5v         | +5v  |
| GND         | GND  |
| DIO (DATA)  | 18   |
| SCK (CLOCK) | 23   |
| RCK (LATCH) | 24   |

Reference:

- [74HC595](http://domoticx.com/arduino-display-module-8x7-segmenten-75hc595/)
- [GPIO](https://www.raspberrypi.org/documentation/usage/gpio/)

## Requirements
- [Pi7SegPy](https://pypi.org/project/Pi7SegPy/)
- [python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib)


