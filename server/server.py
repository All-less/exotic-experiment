#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
import tornado.auth
import config
import os, json, md5, random, base64

from lsqlite import db
from FPGAServer import FPGAServer, Connection, Type
from ExDict import ExDict, DefaultDict
import models
from models import User

class BaseHttpHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Server', 'ExoticServer/0.0.1')
        self.set_header('X-Frame-Options', 'SAMEORIGIN')
        self.set_header('X-XSS-Protection', '1; mode=block')
        self.set_header('x-content-type-options', 'nosniff')

    def get_current_name(self):
        identity = self.get_secure_cookie(config._identity)
        if identity is not None and len(identity) == 32:
            return self.get_secure_cookie(config._user)
        return None

    def set_current_name(self, name):
        self.set_secure_cookie(config._user, name)

    def get_current_user(self):
        identity = self.get_secure_cookie(config._identity)
        if identity is not None and len(identity) == 32:
            return self.get_secure_cookie(config._nickname)
        return None

    def set_current_user(self, user):
        self.set_secure_cookie(config._nickname, user)

    def is_admin(self):
        user = User.get(self.get_current_name())
        return user is not None and user.admin

import UserHandler
import AdminHandler

class HomePage(BaseHttpHandler):
    def get(self):
        user = self.get_current_user()
        self.render('index.html', user=user, status = Connection.status())

class LivePage(BaseHttpHandler):
    @tornado.web.authenticated
    def get(self, id):
        if not Connection.client_valid(id):
            raise tornado.web.HTTPError(404)
        user = self.get_current_user()
        self.render('live.html', username=user)

class LivePageFile(BaseHttpHandler):
    def get(self, index = None, action = None):
        if not Connection.client_valid(index):
            raise tornado.web.HTTPError(404)
        index = int(index)
        status = Connection.client[index].file_status()
        if action == 'download':
            if status.valid:
                self.set_header('Content-Type', 'application/force-download')
                self.set_header('Content-Length', status.size)
                self.set_header('Content-Disposition', 'attachment; filename=%s' % str(status.name))
                self.write(Connection.client[index]._file.body)
            else:
                raise tornado.web.HTTPError(404)
        else:
            self.write(json.dumps(Connection.client[index].file_status()))
        self.finish()

    def post(self, index = None):
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
            for meta in file_metas:
                filename = meta['filename']
                Connection.client[index].file_add(filename, meta['body'])
            broadcast = dict(
                action = Type.user,
                behave = 'file_upload',
                info = Connection.client[index].file_status()
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
        username = self.get_current_user()
        if username is None or not Connection.client_valid(index):
            self.close()
        self._liver = Connection.client[int(index)]
        self.username = username
        self.identity = self.get_secure_cookie(config._identity, None)
        self._liver.user_add(self)
        print 'New web client: %s@%d' % (username, self._liver._index)

    def on_message(self, message):
        try:
            print '%s@%d%s:' % (self.get_current_user(), self._liver._index, '#' if self._liver.admin_handle_check(self) else '$'), message
            message = str(message)
            obj = json.loads(message)
            action = obj.get('action', None)
            if action == Type.user:
                behave = obj.get('behave', '')
                if behave == 'acquire':
                    self._liver.admin_acquire(self)
                elif behave == 'release':
                    self._liver.admin_release(self)
            else:
                if self._liver.admin_handle_check(self):
                    self._liver.broadcast_messages(message)
                    self._liver.send_message(message)
        except Exception as e:
            print e

    def on_close(self):
        self._liver.user_remove(self)

class ApiLiveListHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(Connection.status()))

class ApiStatusHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(dict(
            socketport = config.socketport
        )))
        self.finish()

if __name__ == '__main__':
    config.show()
    db.create_engine(config.database)
    app = tornado.web.Application([
            (r'/', HomePage),
            (r'/live/(.*)/', LivePage),
            (r'/live/(.*)/file', LivePageFile),
            (r'/live/(.*)/file/(.*)', LivePageFile),
            (r'/socket/live/(.*)/', LiveShowHandler),
            (r'/api/livelist', ApiLiveListHandler),
            (r'/api/status', ApiStatusHandler),
            (r'/api/admin/query', AdminHandler.FPGAQueryHttpHandler),
            (r'/api/admin/add', AdminHandler.FPGAAddHttpHandler),
            (r'/admin/add', AdminHandler.FPGAAddHttpHandler),
            (r'/register', UserHandler.RegisterHandler),
            (r'/login', UserHandler.LoginHandler),
            (r'/logout', UserHandler.LogoutHandler),
        ],
        **config.settings
    )
    app.listen(config.webport)
    server = FPGAServer()
    server.listen(config.socketport)
    tornado.ioloop.IOLoop.instance().start()
