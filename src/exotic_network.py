# -*- coding: utf-8 -*-
import json
import exotic
import exotic_rpi
import exotic_rtmp
import exotic_fpga


param = {'auth': False}
stream = None


def handle_initialization(message):
    param['index'] = exotic.get(message, exotic.AUTH_INDEX)
    param['rtmp_host'] = exotic.get(message, exotic.AUTH_HOST)
    param['rtmp_port'] = exotic.get(message, exotic.AUTH_PUSH)
    param['stream_name'] = exotic.get(message, exotic.AUTH_STREAM)
    param['link'] = exotic.get(message, exotic.AUTH_LINK)
    param['port'] = exotic.get(message, exotic.AUTH_PORT)
    param['auth'] = True
    # TODO: setting up rtmp streaming


def handle_control(message):
    behavior = message.get(exotic.MSG_BEHAVIOR)
    if behavior == exotic.BHV_UPLOAD:
        pass
        # TODO: download the file to FPGA board


def handle_operations(message):
    operation = message.get(exotic.MSG_ACTION)
    # TODO


def process(content):
    try:
        message = json.loads(content)
    except ValueError:
        print 'Failed to receive data correctly.'
        return

    if not param['auth']:
        status = message.get(exotic.MSG_STATUS, None)
        if status == exotic.CODE_SUCCESS:
            handle_initialization(message)
        return

    action = message.get(exotic.MSG_ACTION, None)
    if action == exotic.CODE_CONTROL:
        handle_control(message)
    elif action in exotic.CODE_OPERATIONS:
        handle_operations(message)
    else:
        print 'Illegal action number found in received data.'


def init():
    stream.write(exotic.jsonfy({
        exotic.MSG_ACTION: exotic.CODE_CONTROL,
        exotic.MSG_BEHAVIOR: exotic.BHV_AUTH,
        exotic.MSG_DEVID: exotic.device_id,
        exotic.MSG_AUTHKEY: exotic.auth_key
    }))
    stream.read_until(exotic.delimiter, process)


