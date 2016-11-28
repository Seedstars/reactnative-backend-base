from reactnativebackend.settings.base import *  # NOQA (ignore all errors on this line)

DEBUG = True

PAGE_CACHE_SECONDS = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),  # NOQA (ignore all errors on this line)
    }
}

REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'django_rest_logger.handlers.rest_exception_handler'  # NOQA

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'console': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        }
    },
}

DEFAULT_LOGGER = 'console'

LOGGER_EXCEPTION = DEFAULT_LOGGER
LOGGER_ERROR = DEFAULT_LOGGER
LOGGER_WARNING = DEFAULT_LOGGER
LOGGER_INFO = DEFAULT_LOGGER
