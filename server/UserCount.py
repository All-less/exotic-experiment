#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
from BaseHttpHandler import BaseHttpHandler
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat
import logging, json, urllib, time

class UserCount(object):
	_count = 0

	@classmethod
	def user_add(cls):
		cls._count += 1

	@classmethod
	def user_leave(cls):
		cls._count -= 1

	@classmethod
	def send(cls):
		if config.userCountSend:
			httpclient = AsyncHTTPClient()
			params = dict(
				auth_id = config.device_id,
				auth_key = config.auth_key,
				device_id = config.device_id,
                payload = {
                    "userCount" : cls._count,
                }
			)
			body = urllib.urlencode(params)
			httpclient.fetch(
				request = "http://%s:%d%s" % (config.sendHost, config.sendPort, config.sendURL),
				callback = cls.handle_request,
				method = 'POST',
				body = json.dumps(params),
			)

	@classmethod
	def handle_request(cls, response):
		if response.error:
			logging.info("Report Error. %s %d" % (response.error, cls._count))
		else:
			logging.info("Report Success. %d" % cls._count)

class UserCountHandler(BaseHttpHandler):
	def get(self):
		auth_id = int(self.get_argument('auth_id'))
		auth_key = str(self.get_argument('auth_key'))
		device_id = int(self.get_argument('device_id'))
		report_id = int(self.get_argument('report_id'))
		userCount = int(self.get_argument('userCount'))
		logging.info("GET: %d %d %s %d %d" % (auth_id, device_id, auth_key, report_id, userCount))

	def post(self):
		auth_id = int(self.get_argument('auth_id'))
		auth_key = str(self.get_argument('auth_key'))
		device_id = int(self.get_argument('device_id'))
		report_id = int(self.get_argument('report_id'))
		userCount = int(self.get_argument('userCount'))
		logging.info("POST: %d %d %s %d %d" % (auth_id, device_id, auth_key, report_id, userCount))
