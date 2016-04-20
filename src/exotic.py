# -*- coding: utf-8 -*-
import json
import sys


# Device-related constants
CABLE_NAME = 'JtagHs2'
FPGA_NUMBER = 'XC7K160T'

# Web-related parameters
host = 'exotic.lmin.me'
port = 9007
device_id = 'fpga'
auth_key = 'fc023cab1f61ec4bac259204bf7fe792'
delimiter = '\0'

# Protocol-related constants
KEY_PRESS = 1
SWITCH_ON = 3
SWITCH_OFF = 4
BUTTON_DOWN = 5
BUTTON_UP = 6

CODE_CONTROL = 0
CODE_OPERATIONS = [CODE_CONTROL, KEY_PRESS, SWITCH_ON,
                   SWITCH_OFF, BUTTON_UP, BUTTON_DOWN]
CODE_SUCCESS = 0
CODE_FAILURE = 1

MSG_ACTION = 'action'
MSG_BEHAVIOR = 'behave'
MSG_DEVID = 'device_id'
MSG_AUTHKEY = 'auth_key'
MSG_STATUS = 'status'

BHV_AUTH = 'authorization'
BHV_UPLOAD = 'file_upload'

AUTH_INDEX = 'index'
AUTH_HOST = 'rtmpHost'
AUTH_PUSH = 'rtmpPushPort'
AUTH_STREAM = 'streamName'
AUTH_PORT = 'webport'
AUTH_LINK = 'filelink'


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