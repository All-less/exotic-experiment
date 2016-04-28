# -*- coding: utf-8 -*-
import exotic_rpi as er
import json
import sys
import os
import logging


# shared variable
process = None


# Temporary file
TMP_DIR = 'tmp'
BIT_NAME = 'tmp.bit'
DISK_NAME = 'tmp.disk'
BIT_PATH = os.path.join(TMP_DIR, BIT_NAME)
DISK_PATH = os.path.join(TMP_DIR, DISK_NAME)


# Device-related constants
CABLE_NAME = 'JtagHs2'
FPGA_NUMBER = 'XC7K160T'


# Web-related parameters
host = 'es.lmin.me'
port = 8083
device_id = 'test'
auth_key = '16230156c26d20618e00304958b69942'
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
FIELD_ID = 'id'
FIELD_FILE = 'file'

FIELD_SIZE = 'size'
FIELD_TYPE = 'type'
FIELD_NAME = 'name'
TYPE_BIT = 'bit'
TYPE_DISK = 'disk'

ACT_AUTH = 'authorize'

STAT_AUTHED = 'authorized'
STAT_AUTHFAIL = 'auth_failed'
STAT_UPLOADED = 'file_uploaded'
STAT_PROGRAMMED = 'bit_file_programmed'
STAT_DOWNLOADED = 'disk_file_downloaded'
STAT_KEY = 'key_pressed'
STAT_ON = 'switch_on'
STAT_OFF = 'switch_off'
STAT_PRESSED = 'button_pressed'
STAT_RELEASED = 'button_released'

INFO_CHANGED = 'user_changed'
INFO_USER = 'user'

AUTH_DEVID = 'device_id'
AUTH_AUTHKEY = 'auth_key'
AUTH_INDEX = 'index'
AUTH_HOST = 'rtmp_host'
AUTH_PUSH = 'rtmp_push_port'
AUTH_STREAM = 'stream_name'
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
RPI_INPUTS = [PIN_JAO1, PIN_JAO2, PIN_JAO3, PIN_JAO4, PIN_JAI1, PIN_JAI2, PIN_JAI3, PIN_JAI4]
RPI_OUTPUTS = []
switches = {1: PIN_JAI1, 2: PIN_JAI2, 3: PIN_JAI3, 4: PIN_JAI4}
buttons = {1: PIN_JAO1, 2: PIN_JAO2, 3: PIN_JAO3, 4: PIN_JAO4}


# Utility functions
def jsonfy(arg):
    return json.dumps(arg) + delimiter


def get(obj, key):
    if key in obj:
        return obj[key]
    else:
        raise Exception('Expected field "%s" was not found.' % key)


def create_tmpdir():
    if not os.path.isdir(TMP_DIR):
        os.mkdir(TMP_DIR)
        logging.info('Create temporary directory ' + TMP_DIR + '.')


def clear_tmpdir():
    if not os.path.isdir(TMP_DIR):
        return

    if os.path.isfile(BIT_PATH):
        os.remove(BIT_PATH)
    if os.path.isfile(DISK_PATH):
        os.remove(DISK_PATH)

    try:
        os.rmdir(TMP_DIR)
    except OSError:
        pass
    logging.info('Temporary files and directory cleared.')


def save_tmpfile(path, content):
    if not os.path.isdir(TMP_DIR):
        os.mkdir(TMP_DIR)

    with open(path, 'wb') as f:
        f.write(content)


def exit(ret):
    er.stop_streaming()
    clear_tmpdir()
    sys.exit(ret)


def init_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        filename='exotic.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

