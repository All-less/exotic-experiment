from handlers.base import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        # TODO: check whether the user has logged in
        self.render('index.html')
