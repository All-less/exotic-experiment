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

from tornado.options import define, options
from KeepList import KeepList

define('_user', default='user', help='cookie name of user')
define('webport', default=8080, type=int, help='port at running web server at')
define('socketport', default=8081, type=int, help='port that running socket server at')

class BaseHttpHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Server', 'ExoticServer/0.0.1')
        self.set_header('X-Frame-Options', 'SAMEORIGIN')
        self.set_header('X-XSS-Protection', '1; mode=block')
        self.set_header('x-content-type-options', 'nosniff')

    def get_current_user(self):
        return self.get_secure_cookie(options._user, None)

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

class LiveShowHandler(tornado.websocket.WebSocketHandler):
    def get_current_user(self):
        return self.get_secure_cookie(options._user, None)

    def open(self, index):
        username = self.get_current_user()
        if username is None or not Connection.client_valid(index):
            self.close()
        self._liver = Connection.client[int(index)]
        self.username = username
        self._liver.user_add(self)
        print 'New web client: %s@%d' % (username, self._liver._index)

    def on_message(self, message):
        try:
            print '%s@%d%s:' % (self.get_current_user(), self._liver._index, '#' if self._liver.user_valid(self) else '$'), message
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
                if self._liver.user_valid(self):
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
                    user_number = len(client._user['user'])
                )
                l.append(status)
        return l

    def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self.send_message("hello!!!")
        self.read_message()

        self._index = Connection.client.append(self)
        self._user = dict(
            admin = None,
            lock = thread.allocate_lock(),
            user = set()
        )

        print "A new Liver %s at %d" % (self._address, self._index)

    @classmethod
    def client_valid(cls, index):
        try:
            index = int(index)
            return cls.client[index] is not None
        except:
            return False

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

    def user_valid(self, handle):
        return self._user['admin'] == handle

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
            (r'/live/(.*)', LivePage),
            (r'/socket/live/(.*)', LiveShowHandler),
            (r'/api/livelist', ApiLiveListHandler),
        ],
        **settings
    )
    app.listen(options.webport)
    server = FPGAServer()
    server.listen(options.socketport)
    tornado.ioloop.IOLoop.instance().start()
