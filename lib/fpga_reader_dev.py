#!env/bin/python
# -*- coding: utf-8 -*-
import sys
import json

import RPi.GPIO as GPIO


CLK = 36
CLR = 40
DAT = 38


mapping = [
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


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in [CLK, CLR, DAT]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def validate(res):
    num = res
    for i in range(68):
        if i > 7 and (i - 8) % 10 == 0 and num & 0x1 != 0:
            # print(i)
            return False
        elif i > 12 and (i - 13) % 10 == 0 and num & 0x1 != 1:
            # print(i)
            return False
        num >>= 1
    return True


def extract(res):
    res >>= 4

    led = 0
    for _ in range(4):
        led += res & 0xF
        res >>= 5
    
    segs = []
    for _ in range(8):
        segs.append(res & 0xF)
        res >>= 5

    return led, segs
    
            
def main():

    setup()

    round_ = 0

    while True:

        GPIO.wait_for_edge(CLR, GPIO.RISING)
        GPIO.wait_for_edge(CLR, GPIO.FALLING)

        if round_ == 0:
            res = 0
            valid = False
            for _ in range(68):
                while not GPIO.input(CLK): pass
                res = (res << 1) + (1 if GPIO.input(DAT) else 0)
                while GPIO.input(CLK): pass
                GPIO.wait_for_edge(CLK, GPIO.RISING)
            print('%x' % (res & 0xFFFFFFFFFF))

        elif round_ == 1:
            for shift in [0, 1, 2]:
                if validate(res >> shift):
                    res >>= shift
                    valid = True
                    break
            
        elif round_ == 2 and not valid:
            for shift in [0, 1, 2]:
                if validate(res << shift):
                    res <<= shift
                    valid = True
                    break
        
            
        elif round_ == 3 and valid:
            led, segs = extract(res)
            print(json.dumps({
                'led': led,
                'segs': segs
            }))
            sys.stdout.flush()
        
        round_ = (round_ + 1) % 5       


if __name__ == '__main__':
    main()
