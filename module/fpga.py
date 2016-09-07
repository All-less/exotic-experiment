# -*- coding: utf-8 -*-
import logging
import importlib

from tornado.options import options

from lib import util
import device

logger = logging.getLogger('rpi.' + __name__)

try:
    if options.deploy == 'DEV':
        platform = importlib.import_module('.mock', 'device')
    else:
        platform = importlib.import_module('.' + options.platform, 'device')
except ImportError:
    logger.error('Failed to find corresponding FPGA module named'
                 '{}.py'.format(options.platform), exc_info=True)
    util.exit(1)


def check_alive():
    platform.check_alive()


def program_file(file_path):
    platform.program_file(file_path)


def check_djtgcfg():
    if options.deploy == 'DEV':
        logger.debug('Function "fpga.check_djtgcfg()" called in development mode.')
        return
        
    try:
        res = sp.check_output('djtgcfg', shell=True)
    except sp.CalledProcessError as e:
        res = e.output

    if not res.startswith('ERROR: no command specified'):
        logger.error('The output of command "djtgcfg" is unexpected. '
                     'Please check whether it is correctly installed.')
        util.exit(1)


def init():
    check_djtgcfg()
    check_alive()
    logger.info('Successfully connected to the FPGA board.')
