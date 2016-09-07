#!env/bin/python
# -*- coding: utf-8 -*-
import time
import sys
import random
import math
import json


for i in range(100):
    time.sleep(1)
    print(json.dumps({
        'led': math.floor(random.random() * 0xFFFF),
        'segs': [ math.floor(random.random() * 0x7F) for _ in range(8) ]
    }))
    sys.stdout.flush()
