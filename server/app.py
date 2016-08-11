#!env/bin/python
# -*- coding: utf-8 -*- 
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from settings import settings
from urls import url_patterns


def main():
    app = tornado.web.Application(url_patterns, **settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
