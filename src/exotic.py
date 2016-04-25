# -*- coding: utf-8 -*-
import json
import sys


# Temporary file
TMP_DIR = 'tmp'
TMP_NAME = 'tmp.bit'


# Device-related constants
CABLE_NAME = 'JtagHs2'
FPGA_NUMBER = 'XC7K160T'


# Web-related parameters
"""
host = 'exotic.lmin.me'
port = 9007
"""
host = '10.214.128.116'
port = 8081
device_id = 'test'
auth_key = '1074394f3c93a8c6ebba353ad200790e'
delimiter = '\n'


# Protocol-related constants
KEY_PRESS = 1
SWITCH_ON = 2
SWITCH_OFF = 3
BUTTON_DOWN = 4
BUTTON_UP = 5

TYPE_ACTION = 0
TYPE_STATUS = 1
TYPE_OPERATION = 2
TYPE_INFO = 3

FIELD_ACTION = 'action'
FIELD_STATUS = 'status'
FIELD_INFO = 'info'
FIELD_OPERATION = 'operation'

FIELD_DEVID = 'device_id'
FIELD_AUTHKEY = 'auth_key'
FIELD_ID = 'id'

BHV_AUTH = 'authorization'
BHV_UPLOAD = 'file_upload'

AUTH_INDEX = 'index'
AUTH_HOST = 'rtmpHost'
AUTH_PUSH = 'rtmpPushPort'
AUTH_STREAM = 'streamName'
AUTH_PORT = 'webport'
AUTH_LINK = 'filelink'


# Pin configuration
PIN_JAI1 = 5
PIN_JAI2 = 0
PIN_JAI3 = 3
PIN_JAI4 = 4
PIN_JAO1 = 7
PIN_JAO2 = 0
PIN_JAO3 = 2
PIN_JAO4 = 1
RPI_INPUTS = [PIN_JAO1, PIN_JAO2, PIN_JAO3, PIN_JAO4]
RPI_OUTPUTS = [PIN_JAI1, PIN_JAI2, PIN_JAI3, PIN_JAI4]


# Utility functions
def jsonfy(arg):
    return json.dumps(arg) + delimiter


def get(obj, key):
    if key in obj:
        return obj[key]
    else:
        print 'The server returns erroneous data. \
        Please contact the system administrator.'
        sys.exit()
