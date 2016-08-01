from handlers.base import BaseHandler
from models import User
import logging

logger = logging.getLogger('server.' + __name__)


class HomeHandler(BaseHandler):

    def get(self):
        # TODO: check whether the user has logged in
        self.render('index.html')
        logger.info('GET / 200')
