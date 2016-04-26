# -*- coding: utf-8 -*-
import json
from tornado.httpclient import AsyncHTTPClient
import exotic as ex
import exotic_rtmp
import exotic_fpga as ef
import exotic_rpi as er


status = {'auth': False}
stream = None


def handle_initialization(message):
    status['index'] = ex.get(message, ex.AUTH_INDEX)
    status['rtmp_host'] = ex.get(message, ex.AUTH_HOST)
    status['rtmp_port'] = ex.get(message, ex.AUTH_PUSH)
    status['stream_name'] = ex.get(message, ex.AUTH_STREAM)
    status['link'] = ex.get(message, ex.AUTH_LINK)
    status['port'] = ex.get(message, ex.AUTH_PORT)
    status['auth'] = True


def handle_bit_file(response):
    if response.code != 200:
        print "Failed to download bit file.\n" \
              "Please check your network status or contact the system administrator."
    # TODO:
    # 1. determine where to store bit file
    # 2. add 'with'
    f = open(ex.TMP_DIR + "/" + ex.TMP_NAME, "wb")
    f.write(response.body)
    f.close()
    ef.program_fpga(ex.TMP_DIR + "/" + ex.TMP_NAME)


def handle_disk_file(response):
    if response.code != 200:
        print "Failed to download disk file.\n" \
              "Please check your network status or contact the system administrator."
    # TODO: Move disk file.


def handle_operation(message):
    operation = ex.get(message, ex.FIELD_OPERATION)
    identifier = ex.get(message, ex.FIELD_ID)
    if operation == ex.SWITCH_ON:
        er.rpi_write(ex.switches[identifier], 1)
    elif operation == ex.SWITCH_OFF:
        er.rpi_write(ex.switches[identifier], 0)
    elif operation == ex.BUTTON_DOWN:
        er.rpi_write(ex.buttons[identifier], 1)
    elif operation == ex.BUTTON_UP:
        er.rpi_write(ex.buttons[identifier], 0)
    elif operation == ex.KEY_PRESS:
        # TODO: Integrate PS/2 simulation.
        pass
    else:
        raise


def handle_status(message):
    if ex.get(message, ex.FIELD_STATUS) == ex.STAT_UPLOADED:
        # TODO: Download file.
        # AsyncHTTPClient().fetch('http://' + ex.host + ':' + str(status['port']) +
        #                         status['link'], handle_download)
        pass


def handle_info(message):
    msg_info = ex.get(message, ex.FIELD_INFO)
    if msg_info == ex.INFO_CHANGED:
        if not ex.get(message, ex.INFO_USER):
            exotic_rtmp.start()
        else:
            exotic_rtmp.stop()


def handle_data(data):
    print data
    try:
        message = json.loads(data)
    except ValueError:
        print 'Received data is incorrect.'
        return

    if not status['auth']:
        msg_status = ex.get(message, ex.FIELD_STATUS)
        if msg_status == ex.STAT_AUTHED:
            handle_initialization(message)
        elif msg_status == ex.STAT_AUTHFAIL:
            print "Authorization failed. Please contact the system administrator for for help"
            return
        else:
            raise

    msg_type = ex.get(message, ex.FIELD_TYPE)
    if msg_type == ex.TYPE_OPERATION:
        handle_operation(message)
    elif msg_type == ex.TYPE_STATUS:
        handle_status(message)
    elif msg_type == ex.TYPE_INFO:
        handle_info(message)
    else:
        raise


def init():
    stream.write(ex.jsonfy({
        ex.FIELD_TYPE: ex.TYPE_ACTION,
        ex.FIELD_ACTION: ex.ACT_AUTH,
        ex.AUTH_DEVID: ex.device_id,
        ex.AUTH_AUTHKEY: ex.auth_key
    }))


