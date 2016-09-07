# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import logging

from tornado.escape import json_encode
from tornado.escape import json_decode
from tornado.escape import utf8

from .constant import *

logger = logging.getLogger('tcpserver.' + __name__)


class JsonStream:

    def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self._stream.read_until(bDELIMITER, self.on_read)

    async def on_read(self, data):
        try:
            if data:
                dict_ = json_decode(data)
            await self.on_read_json(dict_)
        except Exception as e:
            logger.error('Error occurs during decoding data from device.\n\
                          {}'.format(e), exc_info=True)
        self._stream.read_until(bDELIMITER, self.on_read)

    def on_read_json(self, dict_):
        pass
        
    def send_json(self, dict_):
        self._stream.write(utf8(json_encode(dict_) + DELIMITER))
