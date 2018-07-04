import base64
import logging
import logging.config
import os
import uuid
import sys

from Crypto.PublicKey import RSA
import tornado
from tornado.options import define, options


def generate_or_get_keys():
    prikey = os.path.join(PROJECT_ROOT, 'keys/', 'private.pem')
    pukey = os.path.join(PROJECT_ROOT, 'keys/', 'public.pem')

    if os.path.exists(prikey) and os.path.exists(pukey):
        with open(prikey, "rb") as file_out:
            private_key = file_out.read()

        with open(pukey, "rb") as file_out:
            public_key = file_out.read()
        return RSA.import_key(private_key), RSA.import_key(public_key)
    else:
        return generate_keys()


def generate_keys():
    """
    RSA modulus length must be a multiple of 256 and >= 1024
    """
    prikey = os.path.join(PROJECT_ROOT, 'keys/', 'private.pem')
    pukey = os.path.join(PROJECT_ROOT, 'keys/', 'public.pem')

    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(prikey, "wb") as file_out:
        file_out.write(private_key)

    public_key = key.publickey().export_key()
    with open(pukey, "wb") as file_out:
        file_out.write(public_key)
    return RSA.import_key(private_key), RSA.import_key(public_key)


def path(root, *ag):
    return os.path.join(root, *ag)


# some basic path settings
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
WCLOUD_PATH = path(PROJECT_ROOT, 'wcloud')
STATIC_PATH = path(PROJECT_ROOT, 'static')
TEMPLATE_PATH = path(PROJECT_ROOT, "templates")
WIT_AUTH_KEY = os.environ.get('WIT_AUTH_KEY')
LOG_DIR = "/var/log/web"


# database settings
DB_NAME = os.environ.get('MYSQL_DATABASE')
DB_USER = os.environ.get('MYSQL_USER')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')

# add project path to system that could importable. eg:
# >>> from web.handlers import base
sys.path.insert(0, BASE_DIR)

# tornado varable define
define("port", default=5000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")


# Development type setting
class DeploymentType:
    PRODUCTION = "PRODUCTION"
    STAGING = "STAGING"
    TEST = "TEST"
    DEV = "DEV"


if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.DEV

# settings for tornado Web class `Application` init
settings = {
    "debug": DEPLOYMENT != DeploymentType.PRODUCTION or options.debug,
    "static_path": STATIC_PATH,
    "template_path": TEMPLATE_PATH,
    "cookie_secret": str(uuid.uuid4().hex),
    "xsrf_cookies": False
}

# logging config
# the dict of below, `root` field is for root logger, `loggers` field are
# child logger. usually, child logger is for diffrence module or scenario.
DEV_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s; %(thread)d - %(filename)s - %(funcName)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'main_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'basic',
            'filename': path(LOG_DIR, 'main.log'),
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'basic',
            'filename': path(LOG_DIR, 'error.log'),
        },
        'requests_main_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'basic',
            'filename': path(LOG_DIR, 'requests_main.log'),
        },
        'requests_error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'basic',
            'filename': path(LOG_DIR, 'requests_error.log'),
        }
    },
    'loggers': {
        'web.foo': {
            'handlers': ['console', 'main_file', 'error_file'],
            'level': 'DEBUG',
            'propogate': False
        },
    },
    'root': {
        'handlers': ['console', 'main_file', 'error_file'],
        'level': 'DEBUG',
    }
}

PROD_LOGGING = DEV_LOGGING.copy()
PROD_LOGGING.update({
    'loggers': {
        'web.foo': {
            'handlers': ['main_file', 'error_file'],
            'level': 'DEBUG',
            'propogate': False
        },
    },
    'root': {
        'handlers': ['main_file', 'error_file'],
        'level': 'DEBUG',
    }
})

LOGGING_CONF = DEV_LOGGING if settings["debug"] else PROD_LOGGING
logging.config.dictConfig(LOGGING_CONF)
