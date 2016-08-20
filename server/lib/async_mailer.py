# -*- coding: utf-8 -*-
from tornado import gen
from tornado.options import options

from async_smtp import SMTP
from async_smtp import SMTPException


class Mailer:

    instance = None

    class _Mailer:

        _smtp = None

        def __init__(self, host, user, password):
            self._host = host
            self._user = user
            self._password = password

        @gen.coroutine
        def check_alive(self):
            if self._smtp:
                try:
                    yield self._smtp.noop()
                    return
                except SMTPException:
                    self._smtp = None
            self._smtp = SMTP()
            yield self._smtp.init(self._host)
            yield self._smtp.login(self._user, self._password)
        
        @gen.coroutine
        def sendmail(self, from_addr, to_addrs, msg):
            yield self.check_alive()
            yield self._smtp.sendmail(from_addr, to_addrs, msg)

    def __new__(cls, host, user, password):
        if not cls.instance:
            cls.instance = cls._Mailer(host, user, password)
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

mailer = Mailer(options.smtp_host, options.mail_addr, options.mail_pass)    
