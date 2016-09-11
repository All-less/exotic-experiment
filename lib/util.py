# -*- coding: utf-8 -*-
import sys

import requests

from module import rpi
from .state import env


def exit(ret):
    rpi.stop_streaming()
    rpi.stop_reading()
    sys.exit(ret)


def download(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception('{}:{}'.format(r.status_code, r.reason))
