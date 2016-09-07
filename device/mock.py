# -*- coding: utf-8 -*-

"""A module simulating a fake FPGA board. 

It can be treated as a template for adding more FPGA devices. That is, 
every specific FPGA driver module should implements functions defined
in this module.
"""

import logging

logger = logging.getLogger('rpi.' + __name__)


def check_alive():
    logger.info('Mock FPGA is alive.')


def program_file(file_path):
    logger.info('Programming file {} to Mock FPGA succeeded.'
                ''.format(file_path))
