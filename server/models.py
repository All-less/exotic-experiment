#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

'''
Models for User, Tweed, Comment, Favorate, Relation.
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
    choose = raw_input(message + '[y/n]')
    return choose in ['y', 'Y', 'Yes', 'yes', 'YES']

class User(Model):
    __table__ = 'users'

    name = StringField(primary_key=True, updatable=False, ddl='varchar(50)')
    nickname = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField(default=False)
    createdAt = FloatField(updatable=False, default=time.time)

    @classmethod
    def new(self, name, nickname, password, admin=False):
        u = User.find_first('where name=?', name);
        if u is None:
            newu = User(name=name, nickname=nickname, password=password_gen(password), admin=admin)
            newu.insert()
            return newu
        else:
            return None

class FPGA(Model):
    __table__ = 'fpga'

    device_id = StringField(primary_key=True, updatable=False, ddl='varchar(50)')
    auth_key = StringField(updatable=False, ddl='varchar(50)')
    createdAt = FloatField(updatable=False, default=time.time)

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
        if not raw_choose('Use default admin config?'):
            name = raw_input("Admin username: ")
            nickname = raw_input("Admin nickname: ")
            password = getpass.getpass("Admin password: ")
        L.append()
        device_id = 'test';
        L.append(FPGA(device_id=device_id, auth_key=auth_key(device_id)))
        for m in L:
            m.insert()
