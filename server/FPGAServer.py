#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
import thread, json, logging
import tornado.tcpserver
from KeepList import KeepList
from ExDict import ExDict, DefaultDict
from models import FPGA

class NotFoundException(Exception):
	pass

class Type:
	user = 0
	keyDown = 1
	keyUp = 2
	switchPress = 3

class Connection(object):
	client = KeepList()
	unauth = DefaultDict(
		head = None,
		tail = None,
		len = 0,
		lock = thread.allocate_lock()
	)

	@classmethod
	def status(cls):
		l = list()
		for index, client in enumerate(cls.client):
			if client is not None:
				status = dict(
					index = index,
					device_id = client.device_id,
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

	@classmethod
	def unauth_add(cls, handle):
		if cls.unauth.len >= config.unauthsize:
			cls.unauth_pop()
		cls.unauth.lock.acquire()
		handle._pre = cls.unauth.tail
		if cls.unauth.head == None:
			cls.unauth.head = handle
		if cls.unauth.tail is not None:
			cls.unauth.tail._nex = handle
		cls.unauth.tail = handle
		cls.unauth.len += 1
		cls.unauth.lock.release()

	@classmethod
	def unauth_pop(cls):
		head = cls.unauth.head
		if head is not None:
			head.send_JSON(dict(
				status = 2,
				message = 'Not authorized exit.'
			))
			head.close()

	@classmethod
	def unauth_remove(cls, handle):
		cls.unauth.lock.acquire()
		pre = handle._pre
		nex = handle._nex
		if pre is not None:
			pre._nex = nex
		if nex is not None:
			nex._pre = pre
		if handle == cls.unauth.head:
			cls.unauth.head = nex
		if handle == cls.unauth.tail:
			cls.unauth.tail = pre
		handle._pre = None
		handle._nex = None
		cls.unauth.len -= 1
		cls.unauth.lock.release()

	@classmethod
	def client_add(cls, handle):
		index = cls.client.append(handle)
		handle._index = index
		handle._user = DefaultDict(
			admin = None,
			lock = thread.allocate_lock(),
			user = set()
		)
		handle._file = DefaultDict(
			name = '',
			body = None
		)

		handle.send_message(json.dumps(dict(
			status = 0,
			index = index,
			webport = config.webport,
			filelink = '/live/%d/file/download' % handle._index
		)))
		handle.authed = True

		logging.info("A new Liver %s at %d" % (handle._address, handle._index))

	def __init__(self, stream, address):
		self._stream = stream
		self._address = address
		self._stream.set_close_callback(self.on_close)
		self._nex = None
		self._pre = None
		self.authed = False
		self.device_id = None

		self._index = -1
		self._user = None
		self._file = None
		Connection.unauth_add(self)
		self.read_message()

	def admin_acquire(self, handle):
		if self._user.admin is None:
			self._user.lock.acquire()
			if self._user.admin is None:
				self._user.admin = handle
				self.broadcast_JSON({
					'action': Type.user,
					'behave': 'user_change',
					'change': handle.nickname
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
		broadcast = True
		logging.info('FPGA-%d: %s' % (self._index, data[:-1]))
		try:
			d = json.loads(data)
			if not self.authed and d['action'] == 0 and d['behave'] == 'authorization':
				fpga = FPGA.find_first("where device_id=? and auth_key=?", d['device_id'], d['auth_key'])
				if fpga is not None:
					broadcast = False
					Connection.unauth_remove(self)
					Connection.client_add(self)
					self.device_id = d['device_id']
				else:
					raise NotFoundException('Not found User')
		except NotFoundException, e:
			self.send_JSON(dict(
				status = 1,
				message = 'not found'
			))
		except:
			pass
		if broadcast and self.authed:
			self.broadcast_messages(data[:-1])
		self.read_message()

	def send_JSON(self, dic):
		self.send_message(json.dumps(dic))

	def send_message(self, data):
		self._stream.write(data)

	def broadcast_JSON(self, data):
		self.broadcast_messages(json.dumps(data))

	def broadcast_messages(self, data):
		for user in self._user.user:
			user.write_message(data)

	def close(self):
		self._stream.close()

	def on_close(self):
		logging.info("Liver %d@%s left" % (self._index, self._address))
		if self.authed:
			self.broadcast_JSON({
				'action': Type.user,
				'behave': 'liver_leave'
			})
			for user in self._user.user:
				user.close()
			Connection.client.remove(self._index)
		else:
			Connection.unauth_remove(self)

class FPGAServer(tornado.tcpserver.TCPServer):
	def handle_stream(self, stream, address):
		logging.info("New connection: %s" % (address,))
		Connection(stream, address)
