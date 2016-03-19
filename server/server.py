#! /usr/bin/env python
#coding=utf-8
import tornado.web
import tornado.ioloop
import tornado.websocket
from tornado.tcpserver import TCPServer
import thread
import os
import json

class Type:
    user = 0
    keyDown = 1
    keyUp = 2
    switchPress = 3

class Index(tornado.web.RequestHandler):
    def get(self):
        user = self.get_cookie('user')
        if (user is None):
            self.render('login.html')
        else:
            self.render('index.html', username=user)

    def post(self):
        self.set_cookie('user', self.get_argument('user'));
        self.redirect('/')

class LiveShowHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    user = None
    userLock = thread.allocate_lock()

    @classmethod
    def userRequire(cls, handle):
        if cls.user is None:
            cls.userLock.acquire()
            if cls.user is None:
                print 'user ', handle.username, ' become the master.'
                cls.user = handle
                cls.sendallJSON({
                    'action': Type.user,
                    'change': handle.username
                })
            cls.userLock.release()

    @classmethod
    def userRelease(cls, handle):
        if cls.user == handle:
            cls.user = None
            cls.sendallJSON({
                'action': Type.user,
                'change': None
            })

    @classmethod
    def userValid(cls, handle):
        return cls.user == handle

    @classmethod
    def sendall(cls, data):
        for client in cls.clients:
            client.write_message(data)

    @classmethod
    def sendallJSON(cls, data):
        cls.sendall(json.dumps(data))

    def open(self):
        username = self.get_cookie('user')
        if username is None:
            self.close()
        self.username = username
        print 'a new web client: ', username
        LiveShowHandler.clients.add(self)

    def on_message(self, message):
        try:
            print message
            obj = json.loads(message)
            action = obj.get('action', None)
            if action == Type.user:
                behave = obj.get('behave', '')
                if behave == 'require':
                    LiveShowHandler.userRequire(self)
                elif behave == 'release':
                    LiveShowHandler.userRelease(self)
            else:
                if LiveShowHandler.userValid(self):
                    LiveShowHandler.sendall(message)
        except e:
            print e
            pass

    def on_close(self):
        LiveShowHandler.clients.remove(self)
        LiveShowHandler.userRelease(self)
'''
class Connection(object):
    client = None

    def __init__(self, stream, address):
        if Connection.client is not None:
            return
        Connection.client = self
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self.send_message("hello!!!")
        self.read_message()
        print "A new Liver", address

    def read_message(self):
        print 'read message'
        self._stream.read_until('\r\n\000', self.broadcast_messages)

    def broadcast_messages(self, data):
        #print "User said:", data[:-1], self._address
        #for conn in Connection.clients:
        #    conn.send_message(data)=
        text = base64.b64encode(data)
        LiveShowHandler.sendall(text)
        print len(text), len(data)
        self.read_message()

    def send_message(self, data):
        self._stream.write(data)

    def on_close(self):
        print "Liver left", self._address
        Connection.client = None

class ChatServer(TCPServer):
    def handle_stream(self, stream, address):
        print "New connection :", address, stream
        Connection(stream, address)
'''

settings = dict(
    cookie_secret = "XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ",
    template_path = os.path.join(os.path.dirname(__file__), "template"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    static_url_prefix = "/static/"
)

if __name__ == '__main__':
    app = tornado.web.Application([
            ('/', Index),
            ('/socket/liveshow', LiveShowHandler),
        ],
        **settings
    )
    app.listen(8080)
    #server = ChatServer()
    #server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
