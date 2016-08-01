from handlers.base import BaseHandler
from models import User


class LoginHandler(BaseHandler):
    # TODO: Implement LoginHandler
    pass


class LogoutHandler(BaseHandler):
    # TODO: Implement LogoutHandler
    pass


class RegisterHandler(BaseHandler):

    def post(self):
        # TODO: Implement RegisterHandler
        self.load_json()
        email = self.get_json_argument('email')
        password = self.get_json_argument('password')
        if User.get(User.email == email):
            self.write()
        else:
            # TODO: Implement cookPassword
            User.create(email=email, password=cookPassword(password)).save()
            self.write()
        self.flush()
