#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
import thread, json
import tornado.tcpserver
from KeepList import KeepList
from ExDict import ExDict, DefaultDict


class Type:
	user = 0
	keyDown = 1
	keyUp = 2
	switchPress = 3

class Connection(object):
	client = KeepList()

	@classmethod
	def status(cls):
		l = list()
		for index, client in enumerate(cls.client):
			if client is not None:
				status = dict(
					index = index,
					admin = client._user.admin is not None,
					user_number = len(client._user.user),
					file = client._file.body is not None
				)
				l.append(status)
		return l

	@classmethod
	def client_valid(cls, index):
		try:
			index = int(index)
			return cls.client[index] is not None
		except:
			return False

	def __init__(self, stream, address):
		self._stream = stream
		self._address = address
		self._stream.set_close_callback(self.on_close)

		self._index = Connection.client.append(self)
		self._user = DefaultDict(
			admin = None,
			lock = thread.allocate_lock(),
			user = set()
		)
		self._file = DefaultDict(
			name = '',
			body = None
		)

		self.send_message(json.dumps(dict(
			index = self._index,
			webport = config.webport,
			filelink = '/live/%d/file/download' % self._index
		)))
		self.read_message()

		print "A new Liver %s at %d" % (self._address, self._index)

	def admin_acquire(self, handle):
		if self._user.admin is None:
			self._user.lock.acquire()
			if self._user.admin is None:
				self._user.admin = handle
				self.broadcast_JSON({
					'action': Type.user,
					'behave': 'user_change',
					'change': handle.username
				})
			self._user.lock.release()

	def admin_release(self, handle):
		if self._user.admin == handle:
			self._user.admin = None
			self.broadcast_JSON({
				'action': Type.user,
				'behave': 'user_change',
				'change': None
			})

	def admin_identity_check(self, string):
		return self._user.admin is not None and self._user.admin.identity == string

	def admin_handle_check(self, handle):
		return self._user.admin == handle

	def file_add(self, filename, file):
		self._file.name = filename
		self._file.body = file

	def file_status(self):
		valid = self._file.body is not None
		size = len(self._file.body) if valid else 0
		return DefaultDict(
			valid = valid,
			size = size,
			name = self._file.name
		)

	def user_add(self, handle):
		self._user.user.add(handle)

	def user_remove(self, handle):
		self._user.user.remove(handle)
		self.admin_release(handle)

	def read_message(self):
		self._stream.read_until('\n', self.on_read)

	def on_read(self, data):
		print 'RPi-%d: ' % (self._index), data[:-1]
		self.broadcast_messages(data[:-1])
		self.read_message()

	def send_message(self, data):
		self._stream.write(data)

	def broadcast_JSON(self, data):
		self.broadcast_messages(json.dumps(data))

	def broadcast_messages(self, data):
		for user in self._user.user:
			user.write_message(data)

	def on_close(self):
		print "Liver %d@%s left" % (self._index, self._address)
		self.broadcast_JSON({
			'action': Type.user,
			'behave': 'liver_leave'
		})
		for user in self._user.user:
			user.close()
		Connection.client.remove(self._index)

class FPGAServer(tornado.tcpserver.TCPServer):
	def handle_stream(self, stream, address):
		#print "New connection :", address, stream
		Connection(stream, address)
