#!/usr/bin/env python


import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import options, parse_command_line, parse_config_file
import logging

from models import Base, engine
from settings import settings
from web.urls import url_patterns


class MainApplication(tornado.web.Application):

    def __init__(self):
        logging.info("init MainApplication with settings: %s" % str(settings))
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    parse_command_line()
    if options.config:
        parse_config_file(options.config)

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    app = MainApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
