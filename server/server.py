#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
import tornado.auth
import config
import os, json, md5, random, base64, logging, time

from lsqlite import db
from FPGAServer import FPGAServer, Connection, Type
from ExDict import ExDict, DefaultDict
import models
from models import User

from BaseHttpHandler import BaseHttpHandler
import UserHandler
import AdminHandler
import UserCount
import LiveHandler

class HomePage(BaseHttpHandler):
    def get(self):
        user = self.get_current_user()
        self.render('index.html', user=user, status = Connection.status())

class ApiLiveListHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(Connection.status()))

class ApiStatusHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(dict(
            socketport = config.socketport,
            rtmpHost = config.rtmpHost,
            rtmpPushPort = config.rtmpPushPort,
            rtmpPullPort = config.rtmpPullPort,
            rtmpAppName = config.rtmpAppName,
            userCount = UserCount.UserCount._count,
            separator = config.separator,
        )))
        self.finish()

if __name__ == '__main__':
    config.show()
    db.create_engine(config.database)
    app = tornado.web.Application([
            (r'/', HomePage),
            (r'/live/(.*)/', LiveHandler.LivePage),
            (r'/live/(.*)/file', LiveHandler.LivePageFile),
            (r'/live/(.*/file/.*)', LiveHandler.LivePageFileDownload, {'path' : config.fileDir}),
            (r'/socket/live/(.*)/', LiveHandler.LiveShowHandler),
            (r'/api/livelist', ApiLiveListHandler),
            (r'/api/status', ApiStatusHandler),
            (r'/api/report', UserCount.UserCountHandler),
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
    tornado.ioloop.PeriodicCallback(UserCount.UserCount.send, config.sendPeriod).start()
    tornado.ioloop.IOLoop.instance().start()
