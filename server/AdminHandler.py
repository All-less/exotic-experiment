#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import tornado.web
import json
import config
from BaseHttpHandler import BaseHttpHandler
import models
from models import FPGA

def require_admin(handler_class):
	def wrap_execute(handler_execute):
		def require_admin(handler):
			valid = handler.is_admin()
			if not valid:
				handler.set_status(401)
				handler._transforms = []
				handler.write(str(tornado.web.HTTPError(401)))
				handler.finish()
			return valid
		def _execute(self, transforms, *args, **kwargs):
			if not require_admin(self):
				return False
			return handler_execute(self, transforms, *args, **kwargs)
		return _execute
	handler_class._execute = wrap_execute(handler_class._execute)
	return handler_class

@require_admin
class BaseAdminHttpHandler(BaseHttpHandler):
	pass

class FPGAQueryHttpHandler(BaseAdminHttpHandler):
	def get(self):
		device_id = self.get_argument('device_id', None)
		d = dict(device_id = device_id)
		if device_id is not None:
			fpga = FPGA.get(device_id)
			if fpga is not None:
				d['status'] = 0
				d['auth_key'] = fpga.auth_key
			else:
				d['status'] = 1
				d['message'] = 'not found'
		else:
			d['status'] = 2
			d['message'] = 'missing device_id'
		self.write(json.dumps(d))
		self.finish()

class FPGAAddHttpHandler(BaseAdminHttpHandler):
	def get(self):
		self.render('FPGAadd.html')

	def post(self):
		device_id = self.get_argument('device_id', None)
		d = dict(device_id = device_id)
		if device_id is not None:
			newf = FPGA.new(device_id)
			if newf is not None:
				d['status'] = 0
				d['auth_key'] = newf.auth_key
			else:
				d['status'] = 1
				d['message'] = 'Already exist'
		else:
			d['status'] = 2
			d['message'] = 'missing device_id'
		self.write(json.dumps(d))
		self.finish()
