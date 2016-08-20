# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging

import tornado.tcpserver

from .device import Device
from .pool import DevicePool

logger = logging.getLogger('server.' + __name__)


class DeviceServer(tornado.tcpserver.TCPServer):

    def handle_stream(self, stream, address):
        logger.info('New device connection from {}.'.format(address))
        device = Device(stream, address)
        DevicePool.add_unauth_device(device)
        
