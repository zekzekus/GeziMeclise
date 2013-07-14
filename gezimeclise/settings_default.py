# Django settings for gezimeclise project.
import os

PROJECT_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = (PROJECT_PATH + "/media/")
MEDIA_URL = '/media/'
STATIC_ROOT = (PROJECT_PATH + "/static/")
STATIC_URL = '/static/'
STATICFILES_DIRS = ((PROJECT_PATH + "/assets/"),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_facebook.context_processors.facebook',
)

AUTHENTICATION_BACKENDS = (
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'gezimeclise.urls'
WSGI_APPLICATION = 'gezimeclise.wsgi.application'
TEMPLATE_DIRS = (PROJECT_PATH + "/gezimeclise/templates/")

#APPS
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_facebook')

GEZI_APPS = (
    'gezimeclise.profiles',
    'gezimeclise.blog',
    'gezimeclise.notifications',
    'gezimeclise.causes')

THIRDPARTY_APPS = (
    'south',
    'taggit',
    'taggit',
    'markitup',
    'celery',
    'djcelery',
    'django-extensions')

INSTALLED_APPS = (DJANGO_APPS +
                  GEZI_APPS +
                  THIRDPARTY_APPS)

#LOGGING
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

#DJANGO-FACEBOOK SETTINGS
AUTH_USER_MODEL = 'profiles.GeziUser'

FACEBOOK_PROFILE_IMAGE_PATH = 'facebook_profiles/%Y/%m/%d'
FACEBOOK_STORE_FRIENDS = True
FACEBOOK_STORE_LIKES = True
FACEBOOK_FORCE_PROFILE_UPDATE_ON_LOGIN = True

#FACEBOOK USERS TO BE GOTTEN BY CELERY
FACEBOOK_CELERY_TOKEN_EXTEND = True
FACEBOOK_CELERY_STORE = True

#MARKITUP
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False})

#BLOG
BLOG_FEED_TITLE = "Gezi Meclise Blog"
BLOG_FEED_DESCRIPTION = "Gezi Meclise Blog"
BLOG_URL = "http://gezimeclise.org/blog/"

#CELERY
import djcelery
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

JQUERY_URL = 'js/jquery1.6-min.js'
FACEBOOK_STORE_LOCAL_IMAGE = False
