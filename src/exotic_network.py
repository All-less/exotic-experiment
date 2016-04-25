# -*- coding: utf-8 -*-
import json
from tornado.httpclient import AsyncHTTPClient
import exotic as ex
import exotic_rtmp
import exotic_fpga as ef
import exotic_rpi as er


param = {'auth': False}
stream = None


def handle_initialization(message):
    param['index'] = ex.get(message, ex.AUTH_INDEX)
    param['rtmp_host'] = ex.get(message, ex.AUTH_HOST)
    param['rtmp_port'] = ex.get(message, ex.AUTH_PUSH)
    param['stream_name'] = ex.get(message, ex.AUTH_STREAM)
    param['link'] = ex.get(message, ex.AUTH_LINK)
    param['port'] = ex.get(message, ex.AUTH_PORT)
    param['auth'] = True
    # TODO: setting up rtmp streaming


def handle_download(response):
    if response.code != 200:
        print "Failed to download bit file.\n" \
              "Please check your network status or contact the system administrator."
    f = open(ex.TMP_DIR + "/" + ex.TMP_NAME, "wb")
    f.write(response.body)
    f.close()
    ef.program_fpga(ex.TMP_DIR + "/" + ex.TMP_NAME)


def handle_control(message):
    behavior = message.get(ex.MSG_BEHAVIOR)
    if behavior == ex.BHV_UPLOAD:
        print param
        AsyncHTTPClient().fetch('http://' + ex.host + ':' + str(param['port']) +
                                param['link'], handle_download)


def handle_operations(message):
    operation = message.get(ex.MSG_ACTION)
    identifier = message.get(ex.MSG_ID)
    if operation == ex.SWITCH_ON:
        er.rpi_write(5, 1)
    elif operation == ex.SWITCH_OFF:
        er.rpi_write(5, 0)
    # TODO


def handle_data(data):
    print data
    try:
        message = json.loads(data)
    except ValueError:
        print 'Received data is incorrect.'
        return

    if not param['auth']:
        status = message.get(ex.MSG_STATUS, None)
        if status == ex.CODE_SUCCESS:
            handle_initialization(message)
        return

    action = message.get(ex.MSG_ACTION, None)
    if action == ex.CODE_CONTROL:
        handle_control(message)
    elif action in ex.CODE_OPERATIONS:
        handle_operations(message)
    else:
        print 'Illegal action number found in received data.'


def init():
    stream.write(ex.jsonfy({
        ex.MSG_ACTION: ex.CODE_CONTROL,
        ex.MSG_BEHAVIOR: ex.BHV_AUTH,
        ex.MSG_DEVID: ex.device_id,
        ex.MSG_AUTHKEY: ex.auth_key
    }))


