"""
https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
https://docs.djangoproject.com/en/1.7/topics/settings/
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Django settings for webapp project.
import os
import sys
import ast # py 2.6 only

def env(key, default=None, valuetype=str, required=False):
    if required and (key not in os.environ):
        raise RuntimeError, u"Required environment setting %s not found" % key
    if valuetype == bool:
        # special handling of booleans: must be a valid python expr: True or False
        raw_val = default
        if key in os.environ:
            raw_val = ast.literal_eval(os.environ.get(key))
    else:
        raw_val = os.environ.get(key, default)
    val = valuetype(raw_val)
    return val


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = env('WEBAPP_SECRET_KEY', required=True)

DEBUG = env('WEBAPP_DEBUG', required=True)

TEMPLATE_DEBUG = env('WEBAPP_TEMPLATE_DEBUG', required=True)

MAIN_DOMAIN = env('WEBAPP_MAIN_DOMAIN', valuetype=unicode, required=True)



LOCAL_APPS = (
    'dashboard',
    'accounting',
    'userman',
    'app',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --
    'filer',
    'easy_thumbnails',
    'crispy_forms',
    'django_facebook',
)
INSTALLED_APPS += LOCAL_APPS


# Thumbnail settings
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3' 

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

WSGI_APPLICATION = 'webapp.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',       
        'NAME':         env('WEBAPP_DB_NAME', required=True),
        'USER':         env('WEBAPP_DB_USER', required=True),
        'PASSWORD':     env('WEBAPP_DB_PASS', required=True),
        'HOST':         env('WEBAPP_DB_HOST', 'localhost'),
        'PORT':         env('WEBAPP_DB_PORT', '3306'), 
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB, optimizer_switch="index_merge_intersection=off", character_set_connection=utf8, collation_connection=utf8_unicode_ci',
            },

    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('WEBAPP_TIME_ZONE', valuetype=str, required=True)

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = env('WEBAPP_MEDIA_ROOT', valuetype=str, required=True)
MEDIA_URL_DOMAIN = env('WEBAPP_MEDIA_URL_DOMAIN', '', valuetype=str, required=True)
MEDIA_URL_PATH = env('WEBAPP_MEDIA_URL_PATH', valuetype=str, required=True)
MEDIA_URL = '//' + MEDIA_URL_DOMAIN + MEDIA_URL_PATH


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = env('WEBAPP_STATIC_ROOT', valuetype=str, required=True)
STATIC_URL_DOMAIN = env('WEBAPP_STATIC_URL_DOMAIN', '', valuetype=str, required=True)
STATIC_URL_PATH = env('WEBAPP_STATIC_URL_PATH', valuetype=str, required=True)
STATIC_URL = '//' + STATIC_URL_DOMAIN + STATIC_URL_PATH


ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '..', '_static'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # ...
    "django_facebook.context_processors.facebook",
    "django.core.context_processors.request",
)

FACEBOOK_APP_ID = "679905488776591"
FACEBOOK_APP_SECRET = "eb2e35f95cb11c1e73d90f76f339e1b5"

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '..', '_templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# required if DEBUG=False, as of Django > 1.5
ALLOWED_HOSTS = [
    MAIN_DOMAIN,
    MEDIA_URL_DOMAIN,
    STATIC_URL_DOMAIN,
    ]

LOGIN_REDIRECT_URL = '/'

EMAIL_FROM = 'SPLASH <noreply@%s>' % MAIN_DOMAIN
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "api.wyrls.net"
EMAIL_PORT = 25

# -- Export Reports
EXPORT_FORMATS = (
    ('xls', 'Excel Format'),
    ('csv', 'CSV Format')
)

MIMETYPE_MAP = {
    'xls': 'application/vnd.ms-excel',
    'csv': 'text/csv',
}


XDN_MESSAGING_API_USER = "u/5/testapp"
XDN_MESSAGING_API_PSWD = "ufSJzHjP68ySByy9CpfZ"
XDN_MESSAGING_API_USAGETYPE = "TEST_NB_FREE"

XDN_MESSAGING_API_URL = "http://api.xdn.localhost/documents"
XDN_MESSAGING_API_CONTENT_TYPE  = "application/vnd.net.wyrls.Document-v3+json"
