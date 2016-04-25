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
    en.handle_data(data)
    en.stream.read_until(ex.delimiter, on_read)


def on_connect():
    en.init()
    en.stream.read_until(ex.delimiter, on_read)


if __name__ == '__main__':
    
    er.rpi_init()
    ef.connect_fpga()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    en.stream = tornado.iostream.IOStream(s)
    en.stream.connect((ex.host, ex.port), en.init)
    tornado.ioloop.IOLoop.current().start()
