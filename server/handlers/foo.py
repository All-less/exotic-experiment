from __future__ import absolute_import 
from .base import BaseHandler

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class FooHandler(BaseHandler):
    def get(self):
        self.render("base.html")
