#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import tornado.iostream
import tornado.ioloop
import exotic as ex
import exotic_network as en
import exotic_fpga as ef
import exotic_rpi as er


def on_read(data):
    print 'on_read() called.'
    try:
        print data
        en.handle_data(data)
    except Exception as e:
        print e
        print 'The server returns erroneous data. \
        \n%s\n Please contact the system administrator.' % (data.strip(), )
    print 'Before on_read()'
    en.stream.read_until(ex.delimiter, on_read)


def on_connect():
    en.init()
    print 'In on_connect(), before read_until'
    en.stream.read_until(ex.delimiter, on_read)


if __name__ == '__main__':
    
    er.rpi_init()
    er.process = None
    ef.connect_fpga()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    en.stream = tornado.iostream.IOStream(s)
    en.stream.connect((ex.host, ex.port), on_connect)
    tornado.ioloop.IOLoop.current().start()
