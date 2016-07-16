import wiringpi as W

CLK = 4
CLR = 8
DAT = 2

pins = [CLK, CLR, DAT]

W.wiringPiSetup()

for pin in pins:
    W.pinMode(pin, W.INPUT)
    W.pullUpDnControl(pin, W.PUD_UP)


IDLE = 1
CLEAR = 2
WORK = 3
state = IDLE
count = 0
content = 0
prev = W.LOW

while True:
    if state == IDLE:
        if W.digitalRead(CLR) == W.HIGH:
            state = CLEAR
    elif state == CLEAR:
        if W.digitalRead(CLR) == W.LOW:
            state = WORK
    elif state == WORK:
        cur = W.digitalRead(CLK) 
        if prev == W.LOW and cur == W.HIGH:
            count += 1
            tmp = W.digitalRead(DAT)
            content = (content << 1) + tmp
        prev = cur
        if count == 40:
            count = 0
            state = IDLE
            print "%X" % content
            content = 0
            prev = W.LOW
