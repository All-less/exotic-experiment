#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
import tornado.web
from BaseHttpHandler import BaseHttpHandler
from FileManager import FileManager
from FPGAServer import Connection, Type
from models import User
import logging, json, time

class LivePage(BaseHttpHandler):
	@tornado.web.authenticated
	def get(self, id):
		if not Connection.client_valid(id):
			raise tornado.web.HTTPError(404)
		id = int(id)
		user = self.get_current_user()
		self.render(
			'live.html',
			nickname=user,
			rtmpHost = config.rtmpHost,
			rtmpPullPort = config.rtmpPullPort,
			rtmpAppName = config.rtmpAppName,
			streamName = Connection.client[id]._streamName
		)

class LivePageFileDownload(tornado.web.StaticFileHandler):
	@classmethod
	def get_absolute_path(cls, root, path):
		return FileManager.getFilePath(path)

	def set_extra_headers(self, path):
		self.set_header('Content-Disposition', 'attachment;')
		self.set_header('Content-Type', 'application/force-download')

class LivePageFile(BaseHttpHandler):
	def get(self, index = None, action = None):
		if not Connection.client_valid(index):
			raise tornado.web.HTTPError(404)
		index = int(index)
		status = Connection.client[index].file_status()
		self.write(json.dumps(Connection.client[index].file_status()))
		self.finish()

	def post(self, index = None):
		if not Connection.client_valid(index):
			raise tornado.web.HTTPError(404)
		index = int(index)
		if not Connection.client[index].admin_identity_check(self.get_secure_cookie(config._identity)):
			raise tornado.web.HTTPError(403)
		try:
			contentlength = int(self.request.headers.get('Content-Length'))
		except:
			contentlength = config.filesize
		if contentlength < config.filesize:
			file_metas = self.request.files.get('file', [])
			for meta in file_metas:
				filename = meta['filename']
				Connection.client[index].file_add(filename, meta['body'])
			broadcast = dict(
				action = Type.user,
				behave = 'file_upload',
				info = Connection.client[index].file_status()
			)
			Connection.client[index].broadcast_JSON(broadcast)
			Connection.client[index].send_message(json.dumps(broadcast))
		else:
			raise tornado.web.HTTPError(403)

class LiveShowHandler(tornado.websocket.WebSocketHandler):
	def get_current_user(self):
		identity = self.get_secure_cookie(config._identity)
		if identity is not None and len(identity) == 32:
			return self.get_secure_cookie(config._nickname)
		return None

	def open(self, index):
		nickname = self.get_current_user()
		if nickname is None or not Connection.client_valid(index):
			self.close()
		self._liver = Connection.client[int(index)]
		self.nickname = nickname
		self.identity = self.get_secure_cookie(config._identity, None)
		self._liver.user_add(self)
		self._timestamp = 0
		logging.info('New web client: %s@%d' % (nickname, self._liver._index))

	def on_message(self, message):
		try:
			logging.info(
				'%s@%d%s: %s' % (
					self.get_current_user(),
					self._liver._index,
					'#' if self._liver.admin_handle_check(self) else '$',
					message
				)
			)
			message = str(message)
			obj = json.loads(message)
			action = obj.get('action', None)
			if action == Type.user:
				behave = obj.get('behave', '')
				if behave == 'acquire':
					self._liver.admin_acquire(self)
				elif behave == 'release':
					self._liver.admin_release(self)
			elif obj.get('broadcast', None) == 1:
				nowtime = int(time.time())
				if nowtime - self._timestamp >= config.messageInterval:
					self._timestamp = nowtime
					obj['timestamp'] = nowtime
					obj['nickname'] = self.nickname
					self._liver.broadcast_JSON(obj)
			else:
				if self._liver.admin_handle_check(self):
					self._liver.broadcast_messages(message)
					self._liver.send_message(message)
		except Exception as e:
			logging.info(str(e))

	def on_close(self):
		self._liver.user_remove(self)
