from adjudiCat.settings.common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'django-insecure-=wkk#zrk*t0x(8h-u$$b=vc2ip2q2dli$kq7!2zz=y4fm8(#xa'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}