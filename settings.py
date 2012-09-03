# Django settings for lobby_adamsschool_com project.
import os
import sys

gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(PROJECT_PATH, 'public')
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))

ADMINS =  (
    ('Colin Powell', 'colin.powell@gmail.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

gettext_noop = lambda s: s
LANGUAGES = [
    ('en', gettext_noop('English')),
]

MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')


MEDIA_URL = "/media/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = os.path.join(PUBLIC_DIR, "static/admin")


from imp import find_module
STATICFILES_DIRS = (
    os.path.join(os.path.abspath(find_module("debug_toolbar")[1]), 'media'),
    os.path.join(os.path.abspath(find_module("superslides")[1]), 'media'),
    os.path.join(PROJECT_PATH, 'static'),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'lobby_adamsschool_com.wsgi.application'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DEBUG_TOOLBAR_MEDIA_ROOT = os.path.join(STATIC_ROOT, 'debug_toolbar')

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=uwxb__g7_w1f7kqznn4fddmgo-y(6)x@fn2lxq(lptb0pqj09'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'lobby_adamsschool_com.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'django_extensions',
    'debug_toolbar',
    'superslides',
    'easy_thumbnails',
)

SUPERSLIDES_ROOT = 'slides'
SUPERSLIDES_SLIDE_SIZE = '1300x800'

THUMBNAIL_ALIASES = {
        '': {
             'slideshow': {'size': (1300, 800), 'crop': False},
            },
}

TINYMCE_DEFAULT_CONFIG = {
        'plugins': "table,spellchecker,paste,searchreplace",
            'theme': "advanced",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from local_settings import *
