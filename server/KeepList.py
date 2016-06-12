#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import thread


class KeepList(list):
    '''
    This list will keep its length when remove.
    And add new node into the removed empty place by default.

    >>> a = KeepList()
    >>> a.append(1001)
    0
    >>> a.append(1002)
    1
    >>> a.append(1003)
    2
    >>> a.remove(0)
    >>> print a
    [None, 1002, 1003]
    >>> a.remove(0)
    Traceback (most recent call last):
        ...
    ValueError: Index 0 is removed before.
    >>> a.remove(3)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    >>> a.append(1004)
    0
    >>> print a
    [1004, 1002, 1003]
    >>> a.remove(0)
    >>> a.remove(2)
    >>> print a
    [None, 1002, None]
    >>> a.append(1005)
    2
    >>> a.append(1006)
    0
    >>> a.append(1007)
    3
    >>> print a
    [1006, 1002, 1005, 1007]
    >>> try:
    ...		a.remove(0)
    ...		a.remove(0)
    ... except:
    ...		pass
    ... finally:
    ...		print a._lock.locked()
    False
    >>> a.remove(a)
    Traceback (most recent call last):
        ...
    ValueError: index should be int, but not <class '__main__.KeepList'>
    '''

    def __init__(self):
        super(list, self).__init__()
        self._pre = list()
        self._head = -1
        self._lock = thread.allocate_lock()

    def append(self, obj):
        try:
            self._lock.acquire()
            if self._head == -1:
                list.append(self, obj)
                self._pre.append(-1)
                index = len(self) - 1
            else:
                index = self._head
                self[index] = obj
                self._head = self._pre[index]
                self._pre[index] = -1
        finally:
            self._lock.release()
            return index

    def remove(self, index):
        try:
            self._lock.acquire()
            if type(index) != int:
                raise ValueError('index should be int, but not %s' % type(index))
            if self[index] is None:
                raise ValueError('Index %d is removed before.' % index)
            self[index] = None
            self._pre[index] = self._head
            self._head = index
        finally:
            self._lock.release()


if __name__ == '__main__':
    import doctest

    print 'Testing ', __file__
    print doctest.testmod()
