import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import options, parse_command_line, parse_config_file
import logging

import settings


class MainApplication(tornado.web.Application):
    """
    Just starts the application with the provided settings.
    """

    def __init__(self):
        logging.info(
            "init MainApplication with settings: %s" % str(settings.settings)
        )

        from web.urls import url_patterns
        tornado.web.Application.__init__(
            self, url_patterns, **settings.settings
        )


def main():
    parse_command_line()
    if options.config:
        parse_config_file(options.config)

    priv, pub = settings.generate_or_get_keys()
    settings.settings['private_key'] = priv
    settings.settings['public_key'] = pub

    from models import Base, engine
    Base.metadata.create_all(engine)

    app = MainApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
