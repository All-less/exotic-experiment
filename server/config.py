#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import json, os
from tornado.options import define, options
from ExDict import DefaultDict

define("config",
 	type=str,
    callback=lambda path: options.parse_config_file(path, final=False),
    help="path to config file")

define('_user',
	default='user', type=str,
	help='cookie name of user')
define('_identity',
	default='identity', type=str,
	help='cookie name of identity')
define('_password',
	default='password', type=str,
	help='cookie name of password')
define('_nickname',
	default='nickname', type=str,
	help='cookie name of nickname')

define('webport',
	default=8080, type=int,
	help='port at running web server at')
define('filesize',
	default=1024 * 1024, type=int,
	help='the maximun file size of user can upload')
define('cookie_secret',
	default="XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ", type=str,
	help='the secret cookie')
define('database',
    default='exotic.db', type=str,
    help='the sqlite database file')
define('messageInterval',
    default=2, type=int,
    help='the minimum interval between two message.')

define('socketport',
	default=8081, type=int,
	help='port that running socket server at')
define('unauthsize',
    default=32, type=int,
    help='the connection number without authorization kept by server.')
define('rtmpHost',
    default='localhost', type=str,
    help='the RTMP server for push video flow.')
define('rtmpPushPort',
    default=6666, type=int,
    help='the RTMP server port for push video flow')
define('rtmpPullPort',
    default=1935, type=int,
    help='the RTMP server port for PULL flow.')
define('rtmpAppName',
    default='live', type=str,
    help='the RTMP server Application name for pull flow')

define('userCountSend',
    default=False, type=bool,
    help='send user number to central server')
define('sendPeriod',
    default=5000, type=int,
    help='the interval of sending')
define('sendHost',
    default='localhost', type=str,
    help='the host of central server')
define('sendPort',
    default=8080, type=int,
    help='the port of central server')
define('sendURL',
    default='/api/report', type=str,
    help='the url that accept user infomation.')
define('device_id',
    default=10000, type=int,
    help='the device_id of this server')
define('auth_key',
    default='None', type=str,
    help='the authenticated key of this server')

settings = DefaultDict(
    cookie_secret = options.cookie_secret,
    template_path = os.path.join(os.path.dirname(__file__), "template"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    static_url_prefix = "/static/",
    login_url = '/login',
    xsrf_cookies = False
)

options.parse_command_line()
globals().update(options.as_dict())

def show():
    print "options = ", json.dumps(options.as_dict(), indent = 4)
    print "settings = ", json.dumps(settings, indent = 4)

if __name__ == '__main__':
	show()
