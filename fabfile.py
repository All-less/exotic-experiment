# -*- coding: utf-8 -*-
import re

from fabric.api import sudo, run, cd, local, put, get, warn


def commit(message='', push='n'):
    """
    Usage:
        $ fab commit:message='commit message and escaping comma\, this way',push=n
    """
    local("git add . && git commit -m '{}'".format(message))
    if push == 'y':
        local("git push")


def deploy():
    stop()
    with cd('/var/www/exotic-rpi'):
        run('git checkout .')
        run('git pull')
    start()


def start():
    with cd('/var/www/exotic-rpi'):
        sudo('bash scripts/daemon.sh start')
        sudo('bash scripts/daemon.sh status')


def stop():
    with cd('/var/www/exotic-rpi'):
        output = sudo('bash scripts/daemon.sh status', warn_only=True)
        if re.search(r'.+is running\.', output):
            sudo('bash scripts/daemon.sh stop')
