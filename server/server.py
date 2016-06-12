#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.websocket

import AdminHandler
import LiveHandler
import UserCount
import UserHandler
import config
from BaseHttpHandler import BaseHttpHandler
from FPGAServer import FPGAServer, Connection
from lsqlite import db


class HomePage(BaseHttpHandler):
    def get(self):
        user = self.get_current_user()
        if user and len(Connection.status()) > 0:
            # TODO replace hard-coded redirection
            self.redirect('/live/0/')
        self.render('index.html', user=user, status=Connection.status(), config=config)


class ApiLiveListHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(Connection.status()))


class ApiStatusHandler(BaseHttpHandler):
    def get(self):
        self.write(json.dumps(dict(
                socketport=config.socketport,
                rtmpHost=config.rtmpHost,
                rtmpPushPort=config.rtmpPushPort,
                rtmpPullPort=config.rtmpPullPort,
                rtmpAppName=config.rtmpAppName,
                userCount=UserCount.UserCount._count,
                separator=config.separator,
        )))
        self.finish()


if __name__ == '__main__':
    config.show()
    db.create_engine(config.database)
    app = tornado.web.Application([
        (r'/', HomePage),
        (r'/live/(.*)/', LiveHandler.LivePage),
        (r'/live/(.*)/file', LiveHandler.LivePageFile),
        (r'/live/(.*/file/.*)', LiveHandler.LivePageFileDownload, {'path': config.fileDir}),
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
