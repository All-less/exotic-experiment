# -*- coding: utf-8 -*-
import logging
import subprocess as sp
import os
import signal

from tornado.options import options

from lib.constant import *
from lib.state import env

logger = logging.getLogger('rpi.' + __name__)


def init():
    if options.deploy == 'DEV':
        logger.debug('Function "rpi.init()" called in development mode.')
        return
    for pin in RPI_INPUTS:
        sp.check_output('gpio mode {} in'.format(pin), shell=True)
        sp.check_output('gpio mode {} up'.format(pin), shell=True)
    for pin in RPI_OUTPUTS:
        sp.check_output('gpio mode {} out'.format(pin), shell=True)
    logger.info('GPIO ports initialization done.')


def write(pin, val):
    if options.deploy == 'DEV':
        logger.debug('Function "rpi.write()" called with pin={}, val={}'
                     'in development mode.'.format(pin, val))
        return
    sp.check_output('gpio write {} {}'.format(pin, val), shell=True)


def start_streaming():
    if options.deploy == 'DEV':
        logger.debug('Function "start_streaming()" called in development mode.')
        return
    if not env['process']:
        rtmp_url = ('rtmp://{rtmp_host}:{rtmp_port}/{rtmp_app}/'
                    '{rtmp_stream}').format(env)
        env['process'] = sp.Popen(
            'raspivid '
            '-n '
            '-mm matrix '
            '-w 1280 '
            '-h 720 '
            '-fps 25 '
            '-g 250 '
            '-t 0 '
            '-b 10000000 '
            '-o - '
            '| ffmpeg '
            '-loglevel quiet '
            '-nostats -y '
            '-f h264 '
            '-i - '
            '-c:v copy '
            '-map 0:0 '
            '-f flv '
            '-rtmp_buffer 100 '
            # '-rtmp_live live '
            '{0}'.format(rtmp_url)
            , stdout=sp.PIPE, shell=True, preexec_fn=os.setsid)
        logger.info('Start streaming to {}.'.format(rtmp_url))


def stop_streaming():
    if options.deploy == 'DEV':
        logger.debug('Function "stop_streaming()" called in development mode.')
        return
    if env['process']:
        os.killpg(os.getpgid(env['process'].pid), signal.SIGTERM)
        env['process'] = None
        logger.info('Stop streaming.')
