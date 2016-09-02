# -*- coding: utf-8 -*-
import sys

import rpi


def exit(ret):
    rpi.stop_streaming()
    sys.exit(ret)
