#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'


class ExDict(dict):
    '''
    A dict regard instance.keyname as instance['keyname'].
    and raise error or return default value when not found.

    >>> a = ExDict();
    >>> print a.notfound
    Traceback (most recent call last):
    ...
    AttributeError: 'Dict' object has no attribute 'notfound'
    >>> a.value = 1
    >>> print a.value
    1
    >>> a.__raiseError__ = False
    >>> print a.notfound
    None
    >>> a.__default__ = 'defaultvalue'
    >>> print a.notfound
    defaultvalue
    '''

    def __init__(self, **kw):
        super(ExDict, self).__init__(**kw)
        self.__raiseError__ = True
        self.__default__ = None

    def __getattr__(self, key):
        if key.startswith('_'):
            return object.__getattr__(self, key)
        try:
            return self[key]
        except KeyError:
            if self.__raiseError__:
                raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
            else:
                return self.__default__

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self[key] = value


class DefaultDict(ExDict):
    '''
    a dict return a preset value when not found.

    >>> a = DefaultDict()
    >>> print a.value
    None
    >>> a.value = 2
    >>> print a.value
    2
    '''

    def __init__(self, **kw):
        super(DefaultDict, self).__init__(**kw)
        self.__raiseError__ = False


if __name__ == '__main__':
    import doctest

    print 'Testing ', __file__
    print doctest.testmod()
