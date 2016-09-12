#!env/bin/python
# -*- coding: utf-8 -*-
from tornado.options import options
from tornado.ioloop import IOLoop

from lib import util
import settings
from module import rpi
from module import fpga
from module import network


def main():
    util.setup_trap()
    rpi.init()
    fpga.init()
    network.init(options.host, options.port)
    IOLoop.current().start()


if '__main__' == __name__:
    main()
