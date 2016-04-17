#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
import tornado.web
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
