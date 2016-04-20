#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import tornado.iostream
import tornado.ioloop
import exotic
import exotic_network as en
import exotic_fpga as ef


if __name__ == '__main__':

    ef.connect_fpga()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    en.stream = tornado.iostream.IOStream(s)
    en.stream.connect((exotic.host, exotic.port), en.init)
    tornado.ioloop.IOLoop.current().start()