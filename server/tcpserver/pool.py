# -*- coding: utf-8 -*-
from collections import OrderedDict
import logging

from lib.constant import *

logger = logging.getLogger('server.' + __name__)


class DevicePool:

    devices_to_auth = OrderedDict()
    devices_auth_yet = {}

    @classmethod
    def add_unauth_device(cls, device):
        """Add an unauthenticated device to to-auth list."""
        if len(cls.devices_to_auth) > 100:
            _, first = cls.devices_to_auth.popitem()
            first.send_json({'type': TYPE_INFO, 'info': 'AUTH_TIMEOUT'})
            first.close()
        cls.devices_to_auth[device.id_] = device

    @classmethod
    def auth_device(cls, device):
        """Move the authenticated device from waiting-list to device pool."""
        del cls.devices_to_auth[device.id_]
        cls.devices_auth_yet[device.device_id] = device

    @classmethod
    def remove_authed_device(cls, device):
        """Remove a device from device pool."""
        if device.device_id in cls.devices_auth_yet:
            del cls.devices_auth_yet[device.device_id]

    @classmethod
    def remove_unauth_device(cls, device):
        """Remove a device from to-auth list."""
        if device.id_ in cls.devices_to_auth:
            del cls.devices_to_auth[device.id_]

    @classmethod
    def get_authed_device(cls, device_id):
        return cls.devices_auth_yet[device_id]

    @classmethod
    def get_authed_list(cls):
        return cls.devices_auth_yet.keys()
