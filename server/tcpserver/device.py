# -*- coding; utf-8 -*-
from __future__ import absolute_import, print_function
import uuid
import logging

from tornado.options import options

from lib.constant import *
from lib.json_stream import JsonStream
from models import Rpi
from .pool import DevicePool

logger = logging.getLogger('server.' + __name__)


class Device(JsonStream):

    id_ = None
    device_id = None
    audience = set()
    operator = None

    def __init__(self, stream, address):
        stream.set_close_callback(self.on_close)
        super().__init__(stream, address)
        self.id_ = uuid.uuid4()

    async def on_read_json(self, dict_):
        if not self.device_id:
            await self.check_auth(dict_)
        else:
            self.broadcast_json(dict_)

    async def check_auth(self, dict_):
        if dict_.get('type') == TYPE_STATUS and dict_.get('action') == 'authorize':
            device_id = dict_.get('device_id')
            auth_key = dict_.get('auth_key')
            rpi = await Rpi.find_one({'device_id': device_id})
            if not rpi or rpi['auth_key'] != auth_key:
                self.send_json({
                    'type': TYPE_STATUS, 
                    'status': 'auth_failed'
                })
                return
            self.device_id = device_id
            DevicePool.auth_device(self)
            # TODO
            """
            self.send_json({
                'type': 'status', 
                'status': 'authorized', 
                'webport': options.port,
                'filelink': ,
                'rtmp_port': ,
                'rtmp_host': ,
                'stream_name': 
            })
            """
            logger.info('Device "{}" authentication succeeded.'.format(device_id))

    def join_audience(self, handler):
        self.audience.add(handler)

    def leave_audience(self, handler):
        self.audience.remove(handler)

    def on_close(self):
        if self.device_id:
            DevicePool.remove_authed_device(self)
        else:
            DevicePool.remove_unauth_device(self)


