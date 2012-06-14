# Django settings for LabSense project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jason Tsao', 'jtsao22@ucla.edu'),
)

MANAGERS = ADMINS

SERVER_DIR = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(SERVER_DIR, "LabSenseDB")

#SOCKETIO_HOST = "localhost"
#SOCKETIO_PORT = "8080"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': DB,                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = ''

STATIC_ROOT = os.path.join(SERVER_DIR, 'static')

STATIC_URL = os.path.join(SERVER_DIR, 'static/')

STATICFILES_DIRS = (
    os.path.join(SERVER_DIR, 'LabSenseApp/static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '644$5qu@%%d()$)=ie2^1%$6w=u%k+csjgt^9kaofa)-f$t^sc'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'LabSenseServer.urls'

TEMPLATE_DIRS = (
    os.path.join(SERVER_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'LabSenseApp',
    #'django_socketio',
    #'chat',
    'django.contrib.admin',
    'django.contrib.admindocs',
)
