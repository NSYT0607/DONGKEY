from .common import *

DEBUG = False
ALLOWED_HOSTS = ['52.79.117.221']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'DONGKey',
        'USER': 'NSY',
        'PASSWORD': '',
    },
}
