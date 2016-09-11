# -*- coding: utf-8 -*-
import logging
import socket
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import tornado.iostream
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import options
from tornado.httpclient import AsyncHTTPClient

from lib.json_stream import JsonStream
from lib.state import env
from lib.download import download
from lib.constant import *
from lib import util
from . import rpi
from . import fpga

logger = logging.getLogger('rpi.' + __name__)


class _Client(JsonStream):

    host = None
    port = None
    connection_failures = 0  # number of reconnection
                             # it will be checked in connect(), incremented in
                             # on_close(), cleared in on_connect()
    download_failures = 0
    keep_alive = None  # Periodical callback to keep connection alive

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.keep_alive = PeriodicCallback(self.report_input, 120000)
        self.connect()

    def connect(self):
        if self.connection_failures > 3:
            logger.error('Reconnection failed for three times.')
            util.exit(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(sock)
        stream.set_close_callback(self.on_close)
        stream.connect((self.host, self.port), self.on_connect)
        try:
            super(_Client, self).__init__(stream)
        except ConnectionRefusedError:
            self.on_close()

    def on_close(self):
        env['auth'] = False
        env['feedback'] = None
        self.connection_failures += 1
        self.keep_alive.stop()
        IOLoop.current().call_later(5, self.connect)

    def on_connect(self):
        self.connection_failures = 0
        self.keep_alive.start()
        logger.info('Connected to {}:{}.'.format(
            self.host, self.port))
        self.try_authenticate()

    def try_authenticate(self):
        if not env['auth']:
            self.authenticate()
            IOLoop.current().call_later(60, self.try_authenticate)

    def authenticate(self):
        self.send_json({
            'type': ACT_AUTH,
            'device_id': options.device_id,
            'auth_key': options.auth_key
        })

    def on_read_json(self, dict_):
        code = dict_.get('type', None)
        if not env['auth']:  # not authenticated yet
            if code == STAT_AUTH_SUCC:
                del dict_['type']
                env.update(dict_)
                env['auth'] = True
                env['feedback'] = self.report_output
                logger.info('Authentication succeeded.')
            elif code == STAT_AUTH_FAIL:
                logger.error('Authentication failed.')
                util.exit(1)
        else:
            if code == INFO_USER_CHANGED:
                user = dict_.get('user', None)
                env['operator'] = user
                if user:
                    logger.info('Device controlled by {}.'.format(user))
                    rpi.start_feedback(env['mode'])
                else:
                    logger.info('Device idle.')
                    rpi.stop_feedback(env['mode'])
                return
            if code == OP_PROG:
                fpga.program_file(env['bit_file'])
                self.send_json({'type': STAT_PROGRAMMED})
                return
            if code == STAT_UPLOADED:
                logger.info('Start downloading file from {}'.format(env['file_url']))
                self.download_failures = 0
                self.download_file()
                return
            if code == ACT_CHANGE_MODE:
                mode = dict_.get('mode', 'digital')
                logger.info('Feedback mode changed to "{}".'.format(mode))
                rpi.switch_mode(mode)
                env['mode'] = mode
                self.send_json({'type': INFO_MODE_CHANGED, 'mode': mode})
                return
            id_ = dict_.get('id', None)
            if code == OP_BTN_DOWN:
                self.toggle_button(id_, 1)
            elif code == OP_BTN_UP:
                self.toggle_button(id_, 0)
            elif code == OP_SW_OPEN:
                self.toggle_switch(id_, 1)
            elif code == OP_SW_CLOSE:
                self.toggle_switch(id_, 0)

    def toggle_button(self, id_, op):
        """
        :param op: 1 means 'press', 0 means 'release'
        """
        if id_ not in BUTTONS:
            return
        if env['buttons'] & pow(2, id_) == op:
            return
        rpi.write(BUTTONS[id_], op)
        env['buttons'] ^= pow(2, id_)
        self.report_input()

    def toggle_switch(self, id_, op):
        """
        :param op: 1 meas 'open', 0 means 'close'
        """
        if id_ not in SWITCHES:
            return
        if env['switches'] & pow(2, id_) == op:
            return
        rpi.write(SWITCHES[id_], op)
        env['switches'] ^= pow(2, id_)
        self.report_input()

    def report_input(self):
        self.send_json({
            'type': STAT_INPUT,
            'buttons': env['buttons'],
            'switches': env['switches']
        })

    def report_output(self, led, segs):
        self.send_json({
            'type': STAT_OUTPUT,
            'led': led,
            'segs': segs
        })

    def download_file(self):
        with ProcessPoolExecutor(max_workers=1) as executor:
            file_name = "{}.bit".format(options.device_id)
            file_path = str(Path(options.tmp_dir) / file_name)
            future = executor.submit(download, env['file_url'], file_path)
            IOLoop.current().add_future(future, self.handle_download_res)

    def handle_download_res(self, future):
        exc = future.exception()
        if exc:
            logger.warning('Error downloading file: {}.'.format(e))
            self.download_failures += 1
            if self.download_failures > 3:
                logger.warning('Failed to download file for 3 times.')
                self.send_json({'type': STAT_DOWNLOAD_FAIL})
                return
            self.download_file()
            return
        file_name = "{}.bit".format(options.device_id)
        file_path = Path(options.tmp_dir) / file_name
        logger.info('File downloaded to {}.'.format(file_path))
        env['bit_file'] = str(file_path)
        self.send_json({'type': STAT_DOWNLOADED})

def init(host, port):
    _Client(host, port)
