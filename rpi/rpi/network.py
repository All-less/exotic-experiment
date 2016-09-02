# -*- coding: utf-8 -*-
import logging
import socket

import tornado.iostream
from tornado.ioloop import IOLoop
from tornado.options import options

from lib.json_stream import JsonStream
from lib.state import env
from lib.constant import *

logger = logging.getLogger('rpi.' + __name__)


class _Client(JsonStream):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        stream = tornado.iostream.IOStream(sock)
        stream.connect((host, port), self.on_connect)
        super(_Client, self).__init__(stream)

    def on_connect(self):
        logger.info('Connected to {}:{}.'.format(
            self.host, self.port))
        self.try_authenticate()

    def try_authenticate(self):
        if not env['auth']:
            self.authenticate()
            IOLoop.current().call_later(60, self.try_authenticate)

    def authenticate(self):
        self.send_json({
            'type': CODE_AUTH,
            'device_id': options.device_id,
            'auth_key': options.auth_key
        })

    def on_read_json(self):
        if not env['auth']:
            pass  # TODO
        else:
            pass  # TODO
            

def init(host, port):
    _Client(host, port)
