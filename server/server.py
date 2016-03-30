#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.tcpserver
import tornado.httpserver
import tornado.options
import tornado.auth
import thread
import os
import json
import re
import md5
import random
import base64

from tornado.options import define, options
from KeepList import KeepList

define('_user', default='user', help='cookie name of user')
define('webport', default=8080, type=int, help='port at running web server at')
define('socketport', default=8081, type=int, help='port that running socket server at')
define('filesize', default=1024 * 1024, type=int, help='the maximun file size of user can upload')

class BaseHttpHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Server', 'ExoticServer/0.0.1')
        self.set_header('X-Frame-Options', 'SAMEORIGIN')
        self.set_header('X-XSS-Protection', '1; mode=block')
        self.set_header('x-content-type-options', 'nosniff')

    def get_current_user(self):
        identity = self.get_secure_cookie('identity')
        if identity is not None and len(identity) == 32:
            return self.get_secure_cookie(options._user)
        return None

    def set_current_user(self, user):
        self.set_secure_cookie(options._user, user)

class Type:
    user = 0
    keyDown = 1
    keyUp = 2
    switchPress = 3

class LoginHandler(BaseHttpHandler):
    def get(self):
        if self.get_current_user() is not None:
            self.redirect('/')
            return
        self.render('login.html')

    def post(self):
        if self.get_current_user():
            raise tornado.web.HTTPError(403)
        # check username and password
        user = self.get_argument('user', None)
        if user is not None:
            self.set_current_user(user)
            m = md5.new()
            m.update(user)
            m.update(str(random.random()))
            print m.hexdigest(), len(m.hexdigest())
            self.set_secure_cookie('identity', m.hexdigest())
            self.redirect(self.get_argument('next', '/'))
        else:
            self.redirect(setting.login_url)

class HomePage(BaseHttpHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        self.render('index.html', username=user, status = Connection.status())

class LivePage(BaseHttpHandler):
    @tornado.web.authenticated
    def get(self, id):
        if not Connection.client_valid(id):
            raise tornado.web.HTTPError(404)
        user = self.get_current_user()
        self.render('live.html', username=user)

class LivePageFile(BaseHttpHandler):

    def get(self, index = None):
        if not Connection.client_valid(index):
            raise tornado.web.HTTPError(404)
        index = int(index)
        status = Connection.client[index].file_status()
        if self.get_argument('download', None) is not None:
            if (status['valid']):
                self.set_header('Content-Type', 'application/force-download')
                self.set_header ('Content-Length', status['size'])
                self.set_header ('Content-Disposition', 'attachment; filename=%s' % str(status['name']))
                self.write(Connection.client[index]._file['body'])
            else:
                raise tornado.web.HTTPError(404)
        else:
            self.write(json.dumps(Connection.client[index].file_status()))
        self.finish()

    def post(self, index = None):
        if not Connection.client_valid(index):
            raise tornado.web.HTTPError(404)
        index = int(index)
        if not Connection.client[index].admin_identity_check(self.get_secure_cookie('identity')):
            raise tornado.web.HTTPError(403)
        try:
            contentlength = int(self.request.headers.get('Content-Length'))
        except:
            contentlength = options.filesize
        if contentlength < options.filesize:
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
            broadcast['file'] =  base64.encodestring(Connection.client[index]._file['body'])
            Connection.client[index].send_message(json.dumps(broadcast))
        else:
            raise tornado.web.HTTPError(403)

class LiveShowHandler(tornado.websocket.WebSocketHandler):

    def get_current_user(self):
        identity = self.get_secure_cookie('identity')
        if identity is not None and len(identity) == 32:
            return self.get_secure_cookie(options._user)
        return None

    def open(self, index):
        username = self.get_current_user()
        if username is None or not Connection.client_valid(index):
            self.close()
        self._liver = Connection.client[int(index)]
        self.username = username
        self.identity = self.get_secure_cookie('identity', None)
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

class Connection(object):
    client = KeepList()

    @classmethod
    def status(cls):
        l = list()
        for index, client in enumerate(cls.client):
            if client is not None:
                status = dict(
                    index = index,
                    admin = client._user['admin'] is not None,
                    user_number = len(client._user['user']),
                    file = client._file is not None
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

    def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)

        self._index = Connection.client.append(self)
        self._user = dict(
            admin = None,
            lock = thread.allocate_lock(),
            user = set()
        )
        self._file = dict(
            name = '',
            body = None
        )

        self.send_message(json.dumps(dict(
            index = self._index
        )))
        self.read_message()

        print "A new Liver %s at %d" % (self._address, self._index)

    def admin_acquire(self, handle):
        if self._user['admin'] is None:
            self._user['lock'].acquire()
            if self._user['admin'] is None:
                self._user['admin'] = handle
                self.broadcast_JSON({
                    'action': Type.user,
                    'behave': 'user_change',
                    'change': handle.username
                })
            self._user['lock'].release()

    def admin_release(self, handle):
        if (self._user['admin'] == handle):
            self._user['admin'] = None
            self.broadcast_JSON({
                'action': Type.user,
                'behave': 'user_change',
                'change': None
            })

    def admin_identity_check(self, string):
        return self._user['admin'] is not None and self._user['admin'].identity == string

    def admin_handle_check(self, handle):
        return self._user['admin'] == handle

    def file_add(self, filename, file):
        self._file['name'] = filename
        self._file['body'] = file

    def file_status(self):
        valid = self._file['body'] is not None
        size = len(self._file['body']) if valid else 0
        return dict(
            valid = valid,
            size = size,
            name = self._file['name']
        )

    def user_add(self, handle):
        self._user['user'].add(handle)

    def user_remove(self, handle):
        self._user['user'].remove(handle)
        self.admin_release(handle)

    def read_message(self):
        self._stream.read_until('\n', self.on_read)

    def on_read(self, data):
        print 'RPi-%d: ' % (self._index), data[:-1]
        self.broadcast_messages(data[:-1])
        self.read_message()

    def send_message(self, data):
        self._stream.write(data)

    def broadcast_JSON(self, data):
        self.broadcast_messages(json.dumps(data))

    def broadcast_messages(self, data):
        for user in self._user['user']:
            user.write_message(data)

    def on_close(self):
        print "Liver %d@%s left" % (self._index, self._address)
        self.broadcast_JSON({
            'action': Type.user,
            'behave': 'liver_leave'
        })
        for user in self._user['user']:
            user.close()
        Connection.client.remove(self._index)

class FPGAServer(tornado.tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        #print "New connection :", address, stream
        Connection(stream, address)

class ApiLiveListHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(Connection.status()))

settings = dict(
    cookie_secret = "XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ",
    template_path = os.path.join(os.path.dirname(__file__), "template"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    static_url_prefix = "/static/",
    login_url = '/login'
)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r'/', HomePage),
            (r'/login', LoginHandler),
            (r'/live/(.*)/', LivePage),
            (r'/live/(.*)/file', LivePageFile),
            (r'/live/(.*)/file/download', LivePageFile),
            (r'/socket/live/(.*)/', LiveShowHandler),
            (r'/api/livelist', ApiLiveListHandler),
        ],
        **settings
    )
    app.listen(options.webport)
    server = FPGAServer()
    server.listen(options.socketport)
    tornado.ioloop.IOLoop.instance().start()
