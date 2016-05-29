#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import json
import logging
import time

import tornado.web

import config
from BaseHttpHandler import BaseHttpHandler
from FPGAServer import Connection, Type
from FileManager import FileManager
from config import Type, Action, Status, Info
from models import User


class LivePage(BaseHttpHandler):
    @tornado.web.authenticated
    def get(self, id):
        if not Connection.client_valid(id):
            raise tornado.web.HTTPError(404)
        id = int(id)
        user = self.get_current_user()
        self.render(
                'live.html',
                nickname=user,
                rtmpHost=config.rtmpHost,
                rtmpPullPort=config.rtmpPullPort,
                rtmpAppName=config.rtmpAppName,
                streamName=Connection.client[id]._streamName
        )


class LivePageFileDownload(tornado.web.StaticFileHandler):
    @classmethod
    def get_absolute_path(cls, root, path):
        try:
            a, b, c = path.split('/')
        except Exception, e:
            raise tornado.web.HTTPError(404)
        print a, b, c
        return FileManager.getFilePath(a, c)

    def set_extra_headers(self, path):
        self.set_header('Content-Disposition', 'attachment;')
        self.set_header('Content-Type', 'application/force-download')


class LivePageFile(BaseHttpHandler):
    def get(self, index=None, action=None):
        if not Connection.client_valid(index):
            raise tornado.web.HTTPError(404)
        index = int(index)
        status = Connection.client[index].file_status()
        self.write(json.dumps(Connection.client[index].file_status()))
        self.finish()

    def post(self, index=None):
        if not Connection.client_valid(index):
            raise tornado.web.HTTPError(404)
        index = int(index)
        if not Connection.client[index].admin_identity_check(self.get_secure_cookie(config._identity)):
            raise tornado.web.HTTPError(403)
        try:
            contentlength = int(self.request.headers.get('Content-Length'))
        except:
            contentlength = config.filesize
        if contentlength < config.filesize:
            file_metas = self.request.files.get('file', [])
            filetype = self.get_argument('filetype', None)
            filemeta = file_metas[-1]
            filename = filemeta['filename']
            Connection.client[index].file_add(filename, filetype, filemeta['body'])
            broadcast = dict(
                    type=Type.status,
                    status=Status.file_upload,
                    file=dict(
                            size=len(filemeta['body']),
                            name=filename,
                            type=filetype
                    )
            )
            Connection.client[index].broadcast_JSON(broadcast)
            Connection.client[index].send_message(json.dumps(broadcast))
        else:
            raise tornado.web.HTTPError(403)


class LiveShowHandler(tornado.websocket.WebSocketHandler):
    def get_current_user(self):
        identity = self.get_secure_cookie(config._identity)
        if identity is not None and len(identity) == 32:
            return self.get_secure_cookie(config._nickname)
        return None

    def open(self, index):
        nickname = self.get_current_user()
        if nickname is None or not Connection.client_valid(index):
            self.close()
        self._liver = Connection.client[int(index)]
        self.nickname = nickname
        self.identity = self.get_secure_cookie(config._identity, None)
        self._liver.user_add(self)
        print self
        self._timestamp = 0
        logging.info('New web client: %s@%d' % (nickname, self._liver._index))

    def on_message(self, message):
        try:
            logging.info(
                    '%s@%d%s: %s' % (
                        self.get_current_user(),
                        self._liver._index,
                        '#' if self._liver.admin_handle_check(self) else '$',
                        message
                    )
            )
            obj = json.loads(message)
            messageType = obj.get("type", None)
            if messageType == Type.action:
                action = obj.get("action", "")
                if action == Action.broadcast:
                    nowtime = int(time.time())
                    if nowtime - self._timestamp >= config.messageInterval:
                        obj['type'] = Type.info
                        del obj['action']
                        obj['info'] = Info.broadcast
                        self._timestamp = nowtime
                        obj['timestamp'] = nowtime
                        obj['nickname'] = self.nickname
                        print obj
                        self._liver.broadcast_JSON(obj)
                elif action == Action.acquire:
                    self._liver.admin_acquire(self)
                elif action == Action.release:
                    self._liver.admin_release(self)
            else:
                if self._liver.admin_handle_check(self):
                    self._liver.send_message(str(message))
        except Exception as e:
            logging.info(str(e))

    def on_close(self):
        self._liver.user_remove(self)
