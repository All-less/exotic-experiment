# -*- coding: utf-8 -*- 
from tornado.options import options
from tornado import gen
from email.mime.text import MIMEText
from async_mailer import mailer
from util import digest_password
from util import gen_vcode
from util import check_password
from util import gen_password
from handlers.base import BaseHandler
from models import User
import logging

logger = logging.getLogger('server.' + __name__)


class LoginHandler(BaseHandler):
    
    @gen.coroutine
    def post(self):
        email = self.get_json_argument('email')
        user = yield User.find_one({'email': email})
        if not user:
            self.fail({'err': 'NO_USER'})
            return
        password = self.get_json_argument('password')
        if not check_password(password, user['salt'], user['password']):
            self.fail({'err': 'WRONG_PASSWORD'})
            return
        self.succ({})


class LogoutHandler(BaseHandler):
    # TODO: Implement LogoutHandler
    pass


class RegisterHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        email = self.get_json_argument('email')
        user = yield User.find_one({'email': email})
        if user:
            self.fail({'err': 'DUPLICATE_EMAIL'})
            return
        salt, cooked = digest_password(self.get_json_argument('password'))
        yield User.insert({'email': email, 'password': cooked, 'salt': salt})
        self.succ({})


class EmailHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        """
        Description:
            Send verification code to the given email.

        Request:
            email: 'xxx@xxx.com'
        """
        user_mail = self.get_json_argument('email')
        code = gen_vcode()
        message = MIMEText('您的验证码为：{}'.format(code))
        message['Subject'] = '【Exotic实验平台】邮箱验证码'
        message['From'] = options.mail_addr
        message['To'] = user_mail
        try:
            # yield mailer.sendmail(options.mail_addr, user_mail, message.as_string())
            logger.info('Verification code: {}'.format(code))
            self.succ({'code': code})
        except Exception as e:
            logger.error('Error: {}'.format(e), exc_info=True)
            self.fail({'err': 'SMTP_ERR'})


class FindPasswordHandler(BaseHandler):
    
    @gen.coroutine
    def post(self):
        email = self.get_json_argument('email')
        user = yield User.find_one({'email': email})
        if not user:
            self.fail({'err': 'NO_USER'})
            return
        password = gen_password()
        salt, cooked = digest_password(password)
        message = MIMEText('您的新登录密码为：{}'.format(password))
        message['Subject'] = '【Exotic实验平台】密码重置提醒'
        message['From'] = options.mail_addr
        message['To'] = email
        try:
            # yield mailer.sendmail(options.mail_addr, user_mail, message.as_string())
            logger.info('New password: {}'.format(password))
        except Exception as e:
            logger.error('Error: {}'.format(e), exc_info=True)
            self.fail({'err': 'SMTP_ERR'})
            return
        yield User.update({'_id': user['_id']}, {'$set': {'password': cooked, 'salt': salt}})
        self.succ({})


class ChangePasswordHandler(BaseHandler):
    
    @gen.coroutine
    def post(self):
        email = self.get_json_argument('email')
        user = yield User.find_one({'email': email})
        if not user:
            self.fail({'err': 'NO_USER'})
            return
        oldpass = self.get_json_argument('oldpass')
        if not check_password(oldpass, user['salt'], user['password']):
            self.fail({'err': 'WRONG_PASSWORD'})
            return
        salt, cooked = digest_password(self.get_json_argument('newpass'))
        yield User.update({'_id': user['_id']}, {'$set': {'password': cooked, 'salt': salt}})
        self.succ({})
