#!env/bin/python
# -*- coding: utf-8 -*- 
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from settings import settings
from urls import url_patterns
from tcpserver.server import DeviceServer


def main():
    app = tornado.web.Application(url_patterns, **settings)
    app.listen(options.http_port)
    tcp = DeviceServer()
    tcp.listen(options.tcp_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
