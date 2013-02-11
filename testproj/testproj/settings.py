import os
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
ROOT_URLCONF = 'testproj.urls'
WSGI_APPLICATION = 'testproj.wsgi.application'
INSTALLED_APPS = ('testapp', 'zcapi',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}
