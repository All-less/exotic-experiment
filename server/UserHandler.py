#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import json

import tornado

import config
import models
from BaseHttpHandler import BaseHttpHandler
from models import User
from FPGAServer import Connection


class BaseUserHttpHandler(BaseHttpHandler):
    def login_as(self, name, password):
        user = User.check(name, password)
        if user is not None:
            self.set_current_name(user.name)
            self.set_current_user(user.nickname)
            self.set_secure_cookie(config._identity, models.auth_key(user.name + user.nickname))
            if len(Connection.status()) > 0:
                self.write(json.dumps({
                    'redirect': '/live/0/'
                }))
            else:
                self.write(json.dumps({
                    'error': 'No available devices.'
                }))
            self.finish()
        else:
            self.redirect(config.settings.login_url)

    def logout(self):
        self.clear_cookie(config._user)
        self.clear_cookie(config._identity)


class LoginHandler(BaseUserHttpHandler):
    def get(self):
        if self.get_current_user() is not None:
            self.redirect('/')
            return
        self.render('login.html', showtype='login', config=config)

    def post(self):
        if self.get_current_user():
            if len(Connection.status()) > 0:
                self.write(json.dumps({
                    'error': 'No available devices.'
                }))
                self.finish()
            # raise tornado.web.HTTPError(403)
        # check username and password
        name = self.get_argument(config._user, None)
        password = self.get_argument(config._password, None)
        self.login_as(name, password)


class RegisterHandler(BaseUserHttpHandler):
    def get(self):
        self.render('login.html', showtype='register', config=config)

    def post(self):
        name = self.get_argument(config._user, None)
        nickname = self.get_argument(config._nickname, None)
        password = self.get_argument(config._password, None)
        user = User.new(name=name, nickname=nickname, password=password)
        self.login_as(name, password)


class LogoutHandler(BaseUserHttpHandler):
    def get(self):
        self.logout()
        self.write(json.dumps({
            'redirect': '/'
        }))
        self.finish()
