# -*- coding: utf-8 -*- 
import logging
import os
from pathlib import Path

import tornado
from tornado.options import define, options

from lib import logconfig
import environment


# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))


define('host', help='host of the server', type=str)
define('port', default=6060, help='port of the server', type=int)

define('debug', default=True, help='debug mode for development', type=bool)
define('deploy', default='DEV', help='DEVelopment or PRODuction mode', type=str)

define('device_id', help='Device ID of RPi for authentication', type=str)
define('auth_key', help='Key phrase for authentication', type=str)

define('config', default=None, help='program configuration', type=str)

define('tmp_dir', default='/tmp/exotic-rpi', help='location for temporary files', type=str)

define('platform', help='FPGA platform connected to this rpi', type=str)

define('cmd_read', default='lib/fpga_reader.py', help='command to start FPGA serial reader program', type=str)
tornado.options.parse_command_line()

if options.config:
    tornado.options.parse_config_file(options.config)


SYSLOG_TAG = "exotic_rpi"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2
LOG_LEVEL = logging.DEBUG if options.debug else logging.INFO
USE_SYSLOG = options.deploy == 'PROD'
# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
   'loggers': {
        'tornado.application': {}, # 
        'tornado.access': {},      # enable default logging
        'tornado.general': {},     #
        'rpi': {
            'level': LOG_LEVEL
        }
    }
}

logconfig.initialize_logging(SYSLOG_TAG, SYSLOG_FACILITY, LOGGERS,
        LOG_LEVEL, USE_SYSLOG)


if not Path(options.tmp_dir).exists():
    try:
        Path(options.tmp_dir).mkdir(parents=True)  # 'exist_ok' not exists in Python3.4
    except FileExistsError:
        pass
