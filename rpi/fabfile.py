# -*- coding: utf-8 -*-
from fabric.api import local


def commit(message='', push='n'):
    """
    Usage:
        $ fab commit:message='commit message and escaping comma\, this way',push=n
    """
    local("git add . && git commit -m '{}'".format(message))
    if push == 'y':
        local("git push")
