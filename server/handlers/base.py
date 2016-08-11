# -*- coding: utf-8 -*- 
import json
import tornado.web
import uuid
import logging

logger = logging.getLogger('server.' + __name__)


class BaseHandler(tornado.web.RequestHandler):

    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            msg = "Could not decode JSON: {}".format(self.request.body)
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                         "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def set_default_headers(self):
        self.set_header('X-Frame-Options', 'SAMEORIGIN')
        self.set_header('X-XSS-Protection', '1; mode=block')
        self.set_header('x-content-type-options', 'nosniff')

    def get_current_user(self):
        # TODO
        pass

    def prepare(self):
        logger.debug("{method} {uri} {body}".format(method=self.request.method, uri=self.request.uri, body=self.request.body))

    def succ(self, data):
        self.write({'code': 0, 'data': data})
        self.flush()

    def fail(self, error):
        self.write({'code': 1, 'error': error})
        self.flush()
