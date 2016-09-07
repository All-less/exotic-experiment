# -*- coding: utf-8 -*-
DELIMITER = '\n'
bDELIMITER = b'\n'

# Pin configuration
PIN_JAI1 = 5
PIN_JAI2 = 0
PIN_JAI3 = 3
PIN_JAI4 = 4
PIN_JAO1 = 7
PIN_JAO2 = 0
PIN_JAO3 = 2
PIN_JAO4 = 1
RPI_INPUTS = []
RPI_OUTPUTS = [PIN_JAO1, PIN_JAO2, PIN_JAO3, PIN_JAO4, 
               PIN_JAI1, PIN_JAI2, PIN_JAI3, PIN_JAI4]
SWITCHES = {0: PIN_JAI1, 1: PIN_JAI2, 2: PIN_JAI3, 3: PIN_JAI4}
BUTTONS = {0: PIN_JAO1, 1: PIN_JAO2, 2: PIN_JAO3, 3: PIN_JAO4}

# Communication protocol
types = [
    'ACT_ACQUIRE', 
    'ACT_RELEASE', 
    'ACT_BROADCAST', 
    'ACT_AUTH', 
    'ACT_SYNC', 
    'ACT_CHANGE_MODE',
    'STAT_AUTH_SUCC', 
    'STAT_AUTH_FAIL', 
    'STAT_INPUT', 
    'STAT_OUTPUT', 
    'STAT_UPLOADED', 
    'STAT_DOWNLOADED',
    'STAT_PROGRAMMED', 
    'OP_BTN_DOWN', 
    'OP_BTN_UP', 
    'OP_SW_OPEN', 
    'OP_SW_CLOSE', 
    'OP_PROG', 
    'INFO_USER_CHANGED', 
    'INFO_DISCONN', 
    'INFO_BROADCAST',
    'INFO_MODE_CHANGED'
]

for i, type_ in enumerate(types):
    exec('{} = {}'.format(type_, i))
