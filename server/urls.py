# -*- coding: utf-8 -*- 
from handlers.home import HomeHandler
from handlers.file import UploadHandler
from handlers.file import DownloadHandler
from handlers.user import LoginHandler
from handlers.user import LogoutHandler
from handlers.user import RegisterHandler
from handlers.base import BaseHandler
from handlers.user import EmailHandler
from handlers.user import FindPasswordHandler
from handlers.user import ChangePasswordHandler
from handlers.platform import PlatformHandler

url_patterns = [
    (r'/api/login', LoginHandler),
    (r'/api/logout', LogoutHandler),
    (r'/api/register', RegisterHandler),
    (r'/api/upload', UploadHandler),
    (r'/api/download', DownloadHandler),
    (r'/api/verify', EmailHandler),
    (r'/api/find', FindPasswordHandler),
    (r'/api/change', ChangePasswordHandler),
    (r'/socket/(.+)', PlatformHandler),
    (r'/(.*)', HomeHandler)
]

"""
(r'/live/(.*)/', LiveHandler.LivePage),
(r'/live/(.*)/file', LiveHandler.LivePageFile),
(r'/live/(.*/file/.*)', LiveHandler.LivePageFileDownload,
 {'path': config.fileDir}),
(r'/socket/live/(.*)/', LiveHandler.LiveShowHandler),
(r'/api/livelist', ApiLiveListHandler),
(r'/api/status', ApiStatusHandler),
(r'/api/report', UserCount.UserCountHandler),
(r'/api/admin/query', AdminHandler.FPGAQueryHttpHandler),
(r'/api/admin/add', AdminHandler.FPGAAddHttpHandler),
(r'/admin/add', AdminHandler.FPGAAddHttpHandler),
(r'/register', UserHandler.RegisterHandler),
(r'/login', UserHandler.LoginHandler),
(r'/logout', UserHandler.LogoutHandler)
"""
