# -*- coding: utf-8 -*-
import logging

import tornado.websocket

from tcpserver.pool import DevicePool

logging.getLogger('server.' + __name__)


class PlatformHandler(tornado.websocket.WebSocketHandler):

    device = None

    def open(self, device_id):
        try:
            self.device = DevicePool.get_authed_device(device_id)
        except KeyError as e:
            self.close(404, 'Invalid device_id')
            logger.warning('Websocket request for invalid device_id\
                            "{}"'.format(device_id))
            return
        self.device.join_audience(self)

    def on_message(self, message):
        pass

    def on_close(self):
        if self.device:
            self.device.leave_audience(self)
