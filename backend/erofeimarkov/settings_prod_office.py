#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .settings_base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'erofeimarkov',
        'HOST': '192.168.10.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'raw_type_999',
    }
}

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'noreply@erofeimarkov.ru'
EMAIL_HOST_PASSWORD = '434390'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
