# -*- coding: utf-8 -*-
import requests

def download(url, file_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception('{}:{}'.format(r.status_code, r.reason))
