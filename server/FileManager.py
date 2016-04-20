#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lmzqwer2'

import config
import os

class FileManager(object):

	@classmethod
	def getFilePath(cls, index):
		return os.path.join(config.fileDir, str(index))

	@classmethod
	def size(cls, index):
		path = cls.getFilePath(index)
		if os.path.exists(path):
			return os.path.getsize(path)
		return 0

	@classmethod
	def write(cls, index, body):
		with open(cls.getFilePath(index), "wb") as f:
			f.write(body)

	@classmethod
	def read(cls, index):
		with open(cls.getFilePath(index), "rb") as f:
			data = f.read()
		return data
