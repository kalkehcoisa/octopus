import os

from tornado.web import (
    StaticFileHandler,
)
from handlers import base
from settings import STATIC_PATH, WCLOUD_PATH

url_patterns = [
    (r"/", base.MainHandler),

    (r'/word_cloud/(.*)', StaticFileHandler, {'path': WCLOUD_PATH}),

    (r'/statics/(.*)', StaticFileHandler, {'path': STATIC_PATH}),
    (r'/css/(.*)', StaticFileHandler, {'path': os.path.join(STATIC_PATH, 'css')}),
    (r'/js/(.*)', StaticFileHandler, {'path': os.path.join(STATIC_PATH, 'js')}),
]
