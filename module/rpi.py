# -*- coding: utf-8 -*-
import logging
import subprocess as sp
import os
import signal
import json

from tornado.options import options
from tornado.process import Subprocess

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
        logger.debug('Function "rpi.write()" called with pin={}, val={} '
                     'in development mode.'.format(pin, val))
        return
    sp.check_output('gpio write {} {}'.format(pin, val), shell=True)


def start_streaming():
    if options.deploy == 'DEV':
        logger.debug('Function "start_streaming()" called in development mode.')
        return
    if not env['process']:
        rtmp_url = ('rtmp://{rtmp_host}:{rtmp_port}/{rtmp_app}/'
                    '{rtmp_stream}').format(**env)
        env['process'] = sp.Popen(
            'raspivid '
            '--nopreview '
            '--metering matrix '
            '-w 800 '
            '-h 600 '
            '-fps 20 '
            '-g 250 '
            '-t 0 '
            '-b 5000000 '
            '-vf '
            '-hf '
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
            '-rtmp_live live '
            '{0}'.format(rtmp_url)
            , shell=True, preexec_fn=os.setsid)
        logger.info('Start streaming to {}.'.format(rtmp_url))


def stop_streaming():
    if options.deploy == 'DEV':
        logger.debug('Function "stop_streaming()" called in development mode.')
        return
    if env['process']:
        os.killpg(os.getpgid(env['process'].pid), signal.SIGTERM)
        env['process'] = None
        logger.info('Stop streaming.')


def start_reading():
    """
    Start reading serial input from FPGA. Every time a transfer completes,
    env['feedback'] will be called with following arguments:

    led: a 16-bit integer
    segs: an array of 8 integers
    """
    if not env['process']:
        if not options.cmd_read:
            logger.waring('No command found for reading output from FPGA.')
            return

        proc = Subprocess(options.cmd_read, shell=True,
                          stdout=Subprocess.STREAM, preexec_fn=os.setsid)

        def on_read(content):
            content = content.decode('utf-8')
            try:
                dict_ = json.loads(content)
                assert len(dict_['segs']) == 8
                assert type(dict_['led']) == int
                if env['feedback']:
                    env['feedback'](dict_['led'], dict_['segs'])
            except (json.JSONDecodeError, AssertionError):
                logger.warning('Received error data from "fpga_reader.py":'
                               ' {}'.format(content))
            if env['process']:
                try:
                    proc.stdout.read_until(b'\n', on_read)
                except BrokenPipeError:
                    pass

        proc.stdout.read_until(b'\n', on_read)
        env['process'] = proc.proc
        logger.info('Start reading serial input from FPGA.')


def stop_reading():
    if env['process']:
        os.killpg(os.getpgid(env['process'].pid), signal.SIGTERM)
        env['process'] = None
        logger.info('Stop reading serial input from FPGA.')


def switch_mode(mode):
    if env['mode'] == mode:
        return
    if mode == 'video' and env['operator']:
        stop_reading()
        start_streaming()
    elif mode == 'digital' and env['operator']:
        stop_streaming()
        start_reading()


def start_feedback(mode):
    if mode == 'video':
        start_streaming()
    elif mode == 'digital':
        start_reading()


def stop_feedback(mode):
    if mode == 'video':
        stop_streaming()
    elif mode == 'digital':
        stop_reading()
