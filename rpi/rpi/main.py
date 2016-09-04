#!env/bin/python
# -*- coding: utf-8 -*-
from tornado.options import options
from tornado.ioloop import IOLoop

from lib import util
import settings
import rpi
import fpga
import network


def main():
    rpi.init()
    fpga.init()
    network.init(options.host, options.port)
    try:
        IOLoop.current().start()
    except:  # make sure resources can be released
        util.exit(0)
    

if '__main__' == __name__:
    main()
