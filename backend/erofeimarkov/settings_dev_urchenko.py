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

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'noreply@erofeimarkov.ru'
EMAIL_HOST_PASSWORD = '434390'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
