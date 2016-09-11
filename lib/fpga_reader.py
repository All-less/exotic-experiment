#!env/bin/python
# -*- coding: utf-8 -*-
import time
import json
import sys

import serial


dig2seg = [
    0b00111111,
    0b00000110,
    0b01011011,
    0b01001111,
    0b01100110,
    0b01101101,
    0b01111101,
    0b00000111,
    0b01111111,
    0b01101111,
    0b01110111,
    0b01111100,
    0b00001111,
    0b01011110,
    0b01111001,
    0b01110001
]


def extract(res):
    led = res[0] + (res[1] << 8)
    segs = []
    for i in range(2, 6):
        segs.insert(0, dig2seg[res[i] & 0xF])
        segs.insert(0, dig2seg[res[i] >> 4])
    return led, segs


def main():
    opts = dict(
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        rtscts=False,
        dsrdtr=False,
        xonxoff=False
    )
    with serial.Serial('/dev/ttyUSB0', **opts) as port:
        while True:
            time.sleep(0.2)
            port.write(b'\x1b')
            res = port.read(6)
            
            led, segs = extract(res)
            print(json.dumps({
                'led': led,
                'segs': segs
            }))
            sys.stdout.flush()


if __name__ == '__main__':
    main()
