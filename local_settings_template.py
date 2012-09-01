LOCAL_DEV = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)

def show_dbg_for_staff(request):
    if request.user.is_staff:
        return True # Always show toolbar, for example purposes only.
    else:
        return False

DEBUG_TOOLBAR_CONFIG = {
    'MEDIA_URL': STATIC_URL + 'debug_toolbar/',
    'SHOW_TOOLBAR_CALLBACK': show_dbg_for_staff,
    'INTERCEPT_REDIRECTS': False,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'HOST': '127.0.0.1',
        'NAME': 'staging_lobby',  # Or path to database file if using sqlite3.
        'USER': 'staging_lobby',
        'PASSWORD': 'fancypassword',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

