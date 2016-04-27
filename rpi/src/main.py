#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import logging
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
        logging.warning('The server returns erroneous data. \
                        Please check your network status.')
        logging.warning(str(e))
        logging.debug('%s' % data.strip())
    en.stream.read_until(ex.delimiter, on_read)


def try_authenticate():
    if not en.status['auth']:
        en.authenticate()
        tornado.ioloop.IOLoop().call_later(60, try_authenticate)


def on_connect():
    logging.info('Successfully connected to ' + ex.host + ':' + str(ex.port) + '.')
    try_authenticate()
    en.stream.read_until(ex.delimiter, on_read)


if __name__ == '__main__':

    logging.basicConfig(filename='exotic.log', level=logging.INFO)
    er.rpi_init()
    er.process = None
    ef.connect_fpga()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    en.stream = tornado.iostream.IOStream(s)
    en.stream.connect((ex.host, ex.port), on_connect)
    tornado.ioloop.IOLoop.current().start()
