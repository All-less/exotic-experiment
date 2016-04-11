#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

'''
Models for User, FPGA board
'''

import time, uuid, hashlib, md5, getpass, random
import config

from lsqlite import db
from lsqlite.db import next_id
from lsqlite.orm import Model, StringField, BooleanField, FloatField, TextField

def auth_key(key):
    m = md5.new()
    m.update(key)
    m.update(str(random.random()))
    return m.hexdigest()

def password_gen(password):
    return hashlib.md5(password).hexdigest()

def raw_choose(message):
    choose = raw_input(message + ' [y/n]')
    return choose.strip().lower() in ['y', 'yes']

class User(Model):
    __table__ = 'users'

    name = StringField(primary_key=True, updatable=False, ddl='varchar(50)')
    nickname = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField(default=False)
    createdAt = FloatField(updatable=False, default=time.time)

    @classmethod
    def new(self, name, nickname, password, admin=False):
        u = User.get(name)
        if u is None:
            newu = User(
                name=name,
                nickname=nickname,
                password=password_gen(password),
                admin=admin
            )
            newu.insert()
            return newu
        else:
            return None

    @classmethod
    def check(cls, name, password):
        return cls.find_first("where name=? and password=?", name, password_gen(password))

class FPGA(Model):
    __table__ = 'fpga'

    device_id = StringField(primary_key=True, updatable=False, ddl='varchar(50)')
    auth_key = StringField(updatable=False, ddl='varchar(50)')
    createdAt = FloatField(updatable=False, default=time.time)

    @classmethod
    def new(self, device_id):
        f = FPGA.get(device_id)
        if f is None:
            newf = FPGA(
                device_id=device_id,
                auth_key=auth_key(device_id)
            )
            newf.insert()
            return newf
        else:
            return None

def getPassword(message):
    password = '2'
    repassword = '1'
    while password != repassword:
        password = getpass.getpass(message)
        repassword = getpass.getpass("Please input again: ")
    return password

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if raw_choose('Initialize all the table in %s?' % config.database):
        L = []
        L.append(User)
        L.append(FPGA)
        db.create_engine(config.database);
        for m in L:
            db.update('drop table if exists %s' % m.__table__)
            db.update(m().__sql__())
        L = []
        name = 'admin'
        nickname = 'Exotic'
        password = 'Exotic'
        device_id = 'test'
        if not raw_choose('Use default config?'):
            name = raw_input("Admin username: ")
            nickname = raw_input("Admin nickname: ")
            password = getPassword("Admin password: ")
            device_id = raw_input("Device_id: ")
        User.new(name, nickname, password, True)
        FPGA.new(device_id)
