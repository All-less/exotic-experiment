#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
import os

class FileManager(object):

	@classmethod
	def getFilePath(cls, index, filetype):
		return os.path.join(config.fileDir, str(index))

	@classmethod
	def size(cls, index, filetype):
		path = cls.getFilePath(index, filetype)
		if os.path.exists(path):
			return os.path.getsize(path)
		return 0

	@classmethod
	def write(cls, index, filetype, body):
		with open(cls.getFilePath(index, filetype), "wb") as f:
			f.write(body)

	@classmethod
	def read(cls, index, filetype):
		with open(cls.getFilePath(index, filetype), "rb") as f:
			data = f.read()
		return data
