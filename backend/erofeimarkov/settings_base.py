#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k8zv4hda+^118s6q26wn_e+jp!xz0w7%u!)5p)i!$w@c(c(jfl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ('www.erofeymarkov.ru', 'www.erofeimarkov.ru', 'erofeimarkov.ru', 'erofeymarkov.ru',)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'catalog',
    'order',
    'notifications',
    'cart',
    'south',
    'mymigrate',
    'productfeeds'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "cart.middleware.cart",
    "erofeimarkov.context_processors.debug",
)

ROOT_URLCONF = 'erofeimarkov.urls'

WSGI_APPLICATION = 'erofeimarkov.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader')
    

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'deploystatic')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTHENTICATION_BACKENDS = (
    'authentication.auth.ModelBackend',
)

AUTH_USER_MODEL = 'authentication.User'

TASTYPIE_DEFAULT_FORMATS = ['json']

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

