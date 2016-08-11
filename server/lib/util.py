import hashlib
from tornado.options import options
from random import choice
from string import ascii_uppercase, digits, ascii_letters


def cook_password(password, salt):
    saltPos = options.salt_pos
    s = hashlib.sha512()
    s.update(bytes(salt[:saltPos], 'utf-8'))
    s.update(bytes(password, 'utf-8'))
    s.update(bytes(salt[saltPos:], 'utf-8'))
    return s.hexdigest() 

def digest_password(password):
    salt = gen_salt()
    return salt, cook_password(password, salt)

def check_password(password, salt, cooked):
    return cooked == cook_password(password, salt)

def gen_password():
    return ''.join(choice(ascii_letters + digits) for i in range(12))
    
def gen_salt():
    return ''.join(choice(ascii_letters + digits) for i in range(64))

def gen_vcode():
    return ''.join(choice(ascii_uppercase + digits) for i in range(4))
