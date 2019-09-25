import os

from .base import *

SECRET_KEY = '&q2@4%v$6^5po@xnh+c4g62oqsan3jwoitj+)k573!(lje3i8p'

DEBUG = True

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}


# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'haskerapp@gmail.com'
EMAIL_HOST_PASSWORD = 'vubzob-3kacbi-roCxuq'
