import os

from tornado.web import (
    StaticFileHandler,
)
from handlers import main
from settings import STATIC_PATH, WCLOUD_PATH

url_patterns = [
    (r"/", main.MainHandler),

    (r'/word_cloud/(.*)', StaticFileHandler, {'path': WCLOUD_PATH}),

    (r'/statics/(.*)', StaticFileHandler, {'path': STATIC_PATH}),
    (r'/css/(.*)', StaticFileHandler, {'path': os.path.join(STATIC_PATH, 'css')}),
    (r'/js/(.*)', StaticFileHandler, {'path': os.path.join(STATIC_PATH, 'js')}),
]
