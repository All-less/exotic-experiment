# -*- coding: utf-8 -*-
import sys

import rpi
from .state import env


def exit(ret):
    rpi.stop_streaming()
    rpi.stop_reading()
    sys.exit(ret)
