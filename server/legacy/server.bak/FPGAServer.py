#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import json
import logging
import os
import thread

import tornado.tcpserver

import config
from ExDict import DefaultDict
from FileManager import FileManager
from KeepList import KeepList
from UserCount import UserCount
from config import Type, Action, Status, Info
from models import FPGA


class Connection(object):
    client = KeepList()
    unauth = DefaultDict(
            head=None,
            tail=None,
            len=0,
            lock=thread.allocate_lock()
    )

    @classmethod
    def status(cls):
        l = list()
        for index, client in enumerate(cls.client):
            if client is not None:
                status = dict(
                        index=index,
                        device_id=client.device_id,
                        admin=client._user.admin is not None,
                        user_number=len(client._user.user),
                        file=client.file_status(),
                        streamName=client._streamName
                )
                l.append(status)
        return l

    @classmethod
    def client_valid(cls, index):
        try:
            index = int(index)
            return cls.client[index] is not None
        except:
            return False

    @classmethod
    def unauth_add(cls, handle):
        if cls.unauth.len >= config.unauthsize:
            cls.unauth_pop()
        cls.unauth.lock.acquire()
        handle._pre = cls.unauth.tail
        if cls.unauth.head == None:
            cls.unauth.head = handle
        if cls.unauth.tail is not None:
            cls.unauth.tail._nex = handle
        cls.unauth.tail = handle
        cls.unauth.len += 1
        cls.unauth.lock.release()

    @classmethod
    def unauth_pop(cls):
        head = cls.unauth.head
        if head is not None:
            head.send_JSON(dict(
                    type=Type.info,
                    info="no authorization exit."
            ))
            head.close()

    @classmethod
    def unauth_remove(cls, handle):
        cls.unauth.lock.acquire()
        pre = handle._pre
        nex = handle._nex
        if pre is not None:
            pre._nex = nex
        if nex is not None:
            nex._pre = pre
        if handle == cls.unauth.head:
            cls.unauth.head = nex
        if handle == cls.unauth.tail:
            cls.unauth.tail = pre
        handle._pre = None
        handle._nex = None
        cls.unauth.len -= 1
        cls.unauth.lock.release()

    @classmethod
    def client_add(cls, handle):
        index = cls.client.append(handle)
        handle._index = index
        handle._user = DefaultDict(
                admin=None,
                lock=thread.allocate_lock(),
                user=set()
        )
        handle._file = DefaultDict(
                mult=dict()
        )
        handle._streamName = str(index)

        handle.send_JSON(dict(
                type=Type.status,
                status=Status.authorized,
                index=index,
                webport=config.webport,
                filelink='/live/%d/file/' % handle._index,
                rtmp_host=config.rtmpHost,
                rtmp_push_port=config.rtmpPushPort,
                stream_name=handle._streamName
        ))
        handle.authed = True

        logging.info("A new Liver %s at %d" % (handle._address, handle._index))

    def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self._nex = None
        self._pre = None
        self.authed = False
        self.device_id = None

        self._index = -1
        self._user = None
        self._file = None
        self._streamName = None
        Connection.unauth_add(self)
        self.read_message()

    def admin_change_message(self, user):
        sendData = dict(
                type=Type.info,
                info=Info.user_changed,
                user=user
        )
        self.broadcast_JSON(sendData)
        self.send_JSON(sendData)

    def admin_acquire(self, handle):
        if self._user.admin is None:
            self._user.lock.acquire()
            if self._user.admin is None:
                self._user.admin = handle
                self.admin_change_message(handle.nickname)
            self._user.lock.release()

    def admin_release(self, handle):
        if self._user.admin == handle:
            self._user.admin = None
            self.admin_change_message(None)

    def admin_identity_check(self, string):
        return self._user.admin is not None and self._user.admin.identity == string

    def admin_handle_check(self, handle):
        return self._user.admin == handle

    def file_get(self, filetype):
        return FileManager.read(self._index, filetype)

    def file_add(self, filename, filetype, file):
        filetype = str(filetype)
        self._file.mult[filetype] = DefaultDict(
                name=os.path.split(filename)[-1],
                size=len(file)
        )
        FileManager.write(self._index, filetype, file)

    def file_status(self):
        return self._file.mult

    def user_add(self, handle):
        UserCount.user_add()
        self._user.user.add(handle)

    def user_remove(self, handle):
        UserCount.user_leave()
        self._user.user.remove(handle)
        self.admin_release(handle)

    def read_message(self):
        self._stream.read_until(config.separator, self.on_read)

    def on_read(self, data):
        broadcast = True
        data = data[:-config.separatorLen]
        logging.info('FPGA-%d: %s' % (self._index, data))
        try:
            d = json.loads(data)
            if d['type'] == Type.action and d['action'] == Action.authorize:
                broadcast = False
                if not self.authed:
                    fpga = FPGA.find_first("where device_id=? and auth_key=?", d['device_id'], d['auth_key'])
                    if fpga is not None:
                        Connection.unauth_remove(self)
                        Connection.client_add(self)
                        self.device_id = d['device_id']
                    else:
                        raise Exception("not found")
        except Exception, e:
            if not broadcast:
                self.send_JSON(dict(
                        type=Type.status,
                        status=Status.auth_failed
                ))
        if broadcast and self.authed:
            self.broadcast_messages(data)
        self.read_message()

    def send_JSON(self, dic):
        self.send_message(json.dumps(dic))

    def send_message(self, data):
        self._stream.write(data + config.separator)

    def broadcast_JSON(self, data):
        print data
        self.broadcast_messages(json.dumps(data))

    def broadcast_messages(self, data):
        for user in self._user.user:
            user.write_message(data)

    def close(self):
        self._stream.close()

    def on_close(self):
        logging.info("Liver %d@%s left" % (self._index, self._address))
        if self.authed:
            self.broadcast_JSON(dict(
                    type=Type.info,
                    info=Info.fpga_disconnected
            ))
            for user in self._user.user:
                user.close()
            Connection.client.remove(self._index)
        else:
            Connection.unauth_remove(self)


class FPGAServer(tornado.tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        logging.info("New connection: %s" % (address,))
        Connection(stream, address)
