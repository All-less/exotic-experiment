# -*- coding: utf-8 -*- 
from handlers.base import BaseHandler
from models import User
import logging

logger = logging.getLogger('server.' + __name__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render('index.html')
