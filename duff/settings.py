# -*- coding: utf-8 -*-
# Django settings for duff project.

from os import environ, path
from urlparse import urlparse


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sascha Peilicke   ', 'saschpe@suse.de'),
)

MANAGERS = ADMINS

# Default database connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'duff',  # Or path to database file if using sqlite3.
        'USER': 'duff',          # Not used with sqlite3.
        'PASSWORD': 'duff',      # Not used with sqlite3.
        'HOST': '',              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',              # Set to empty string for default. Not used with sqlite3.
    }
}
# Allow to override by OS environment
#if environ.has_key('DATABASE_URL'):
#    url = urlparse(environ['DATABASE_URL'])
#    DATABASES['default'] = {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': url.path[1:],
#        'USER': url.username,
#        'PASSWORD': url.password,
#        'HOST': url.hostname,
#        'PORT': url.port,
#    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.abspath('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.abspath('3rd-party/static/bootstrap'),
    path.abspath('3rd-party/static/jquery')
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's##8my+#s9e9rz(sn#!l51=9cibd$o9#2448qxe_*nhxwsh7fv'

# List of callables that know how to import templates from various sources.
if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
else:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
             'django.template.loaders.app_directories.Loader',
        )),
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Debug Toolbar middleware must come after any other middleware that
    # encodes the response's content (such as GZipMiddleware).
    # Note: Be aware of middleware ordering and other middleware that may
    # intercept requests and return responses. Putting the debug toolbar
    # middleware after the Flatpage middleware, for example, means the toolbar
    # will not show up on flatpages.
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'duff.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'duff.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.abspath('duff/templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # 3rd-party apps:
    'debug_toolbar',
    'south',

    # Local apps:
    #'duff.iptables',
    'duff.libvirt',
)

if DEBUG:
    LOG_FILE_NAME = "development.log"
else:
    LOG_FILE_NAME = "production.log"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d: %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'simple',
            'filename': path.join(path.curdir, 'log', LOG_FILE_NAME),
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        # For performance reasons, SQL logging is only enabled when
        # settings.DEBUG is set to True, regardless of the logging level
        # or handlers that are installed.
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}


# Debug toolbar settings:
INTERNAL_IPS = ('127.0.0.1', '10.120.4.195', '10.123.0.74')

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    # 'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    # 'HIDE_DJANGO_SQL': False,
    # 'ENABLE_STACKTRACES' : False,
}
