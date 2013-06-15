from os.path import dirname, join
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = dirname(__file__)
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_DIR,"gezimeclise.db"),
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    }
}
FACEBOOK_APP_ID = "119801478164980"
FACEBOOK_APP_SECRET = "832b2a63f8a2b6970461e41e674c2696"

