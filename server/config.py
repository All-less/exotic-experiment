#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import json
from tornado.options import define, options

define("config",
 	type=str,
    callback=lambda path: options.parse_config_file(path, final=False),
    help="path to config file")
define('_user',
	default='user', type=str,
	help='cookie name of user')
define('webport',
	default=8080, type=int,
	help='port at running web server at')
define('socketport',
	default=8081, type=int,
	help='port that running socket server at')
define('filesize',
	default=1024 * 1024, type=int,
	help='the maximun file size of user can upload')
define('cookie_secret',
	default="XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ", type=str,
	help='the secret cookie')

options.parse_command_line()
globals().update(options.as_dict())

def show():
	print json.dumps(options.as_dict(), indent = 4);

if __name__ == '__main__':
	show()
