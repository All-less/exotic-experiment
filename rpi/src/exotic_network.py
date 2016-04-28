# -*- coding: utf-8 -*-
import json
import logging
from tornado.httpclient import AsyncHTTPClient
import exotic as ex
import exotic_fpga as ef
import exotic_rpi as er


status = {'auth': False}
stream = None


def send_status(message, **kwargs):
    res = {ex.FIELD_TYPE: ex.TYPE_STATUS, ex.FIELD_STATUS: message}
    for key, value in kwargs.iteritems():
        res[key] = value
    logging.debug('Sent status ' + str(res) + '.')
    stream.write(ex.jsonfy(res))


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
        logging.warning('Failed to download bit file.')
        return
    ex.save_tmpfile(ex.BIT_PATH, response.body)
    logging.info('Successfully download bit file.')
    ef.program_fpga(ex.BIT_PATH)
    send_status('bit_file_programmed')


def handle_disk_file(response):
    if response.code != 200:
        logging.warning('Failed to download disk file.')
        return
    ex.save_tmpfile(ex.DISK_PATH, response.body)
    logging.info('Successfully download disk file.')
    send_status('disk_file_downloaded')


def handle_operation(message):
    operation = ex.get(message, ex.FIELD_OPERATION)
    if operation == ex.KEY_PRESS:
        return
        # TODO: Integrate PS/2 simulation.
    identifier = ex.get(message, ex.FIELD_ID)
    if operation == ex.SWITCH_ON:
        er.rpi_write(ex.switches[identifier], 1)
        send_status('switch_on', id=identifier)
    elif operation == ex.SWITCH_OFF:
        er.rpi_write(ex.switches[identifier], 0)
        send_status('switch_off', id=identifier)
    elif operation == ex.BUTTON_DOWN:
        er.rpi_write(ex.buttons[identifier], 1)
        send_status('button_pressed', id=identifier)
    elif operation == ex.BUTTON_UP:
        er.rpi_write(ex.buttons[identifier], 0)
        send_status('button_release', id=identifier)
    else:
        raise Exception('Unexpected operation %d was found' % operation)


def handle_status(message):
    if ex.get(message, ex.FIELD_STATUS) == ex.STAT_UPLOADED:
        msg_file = ex.get(message, ex.FIELD_FILE)
        msg_type = ex.get(msg_file, ex.FIELD_TYPE)
        if msg_type == ex.TYPE_BIT:
            logging.debug('Start downloading bit file from http://' + ex.host + ':' +
                          str(status['port']) + status['link'] + ex.TYPE_BIT)
            AsyncHTTPClient().fetch('http://' + ex.host + ':' + str(status['port']) +
                                    status['link'] + ex.TYPE_BIT, handle_bit_file)
        elif msg_type == ex.TYPE_DISK:
            logging.debug('Start downloading disk file from http://' + ex.host + ':' +
                          str(status['port']) + status['link'] + ex.TYPE_DISK)
            AsyncHTTPClient().fetch('http://' + ex.host + ':' + str(status['port']) +
                                    status['link'] + ex.TYPE_DISK, handle_disk_file)
        else:
            raise Exception('Unexpected type "%s" was found.' % msg_type)


def handle_info(message):
    msg_info = ex.get(message, ex.FIELD_INFO)
    if msg_info == ex.INFO_CHANGED:
        if ex.get(message, ex.INFO_USER):
            er.start_streaming()
        else:
            er.stop_streaming()


def handle_data(data):
    try:
        message = json.loads(data)
        logging.debug('Received data ' + str(message))
    except ValueError:
        raise Exception('Received data cannot be correctly parsed.')

    if not status['auth']:
        msg_status = ex.get(message, ex.FIELD_STATUS)
        if msg_status == ex.STAT_AUTHED:
            handle_initialization(message)
            logging.info('Authentication succeeded.')
        elif msg_status == ex.STAT_AUTHFAIL:
            logging.error('Authentication failed.')
            return
        else:
            raise Exception('Unexpected status "%s" was found.' % msg_status)

    msg_type = ex.get(message, ex.FIELD_TYPE)
    if msg_type == ex.TYPE_OPERATION:
        handle_operation(message)
    elif msg_type == ex.TYPE_STATUS:
        handle_status(message)
    elif msg_type == ex.TYPE_INFO:
        handle_info(message)
    else:
        raise Exception('Unexpected type "%d" was found.' % msg_type)


def authenticate():
    stream.write(ex.jsonfy({
        ex.FIELD_TYPE: ex.TYPE_ACTION,
        ex.FIELD_ACTION: ex.ACT_AUTH,
        ex.AUTH_DEVID: ex.device_id,
        ex.AUTH_AUTHKEY: ex.auth_key
    }))
    logging.info('Authentication request sent.')
    logging.debug('Sent action ' + str({
        ex.FIELD_TYPE: ex.TYPE_ACTION,
        ex.FIELD_ACTION: ex.ACT_AUTH,
        ex.AUTH_DEVID: ex.device_id,
        ex.AUTH_AUTHKEY: ex.auth_key
    }) + '.')


