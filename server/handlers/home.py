# -*- coding: utf-8 -*- 
from __future__ import print_function
import logging

from handlers.base import BaseHandler
from models import User

logger = logging.getLogger('server.' + __name__)


class HomeHandler(BaseHandler):

    def get(self, *args):
        self.render('index.html')
