#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .settings_dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'erofeimarkov',
        'USER': 'hellpain',
        'PASSWORD': 'hellpain',
        'HOST': 'localhost',
    }
}

# MIDDLEWARE_CLASSES = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE_CLASSES

# DEBUG_TOOLBAR_PATCH_SETTINGS = False
# INTERNAL_IPS = '127.0.0.1'

# CONFIG_DEFAULTS = {
#     'RESULTS_STORE_SIZE': 5000,
#     'PROFILER_MAX_DEPTH': 5000,
#     'SQL_WARNING_THRESHOLD': 20000,
# }

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'noreply@erofeimarkov.ru'
EMAIL_HOST_PASSWORD = '434390'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
