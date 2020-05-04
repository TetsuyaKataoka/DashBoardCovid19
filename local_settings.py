import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_dashboard',
        'USER': 'user_dashboard',
        'PASSWORD': 'dashboard',
        'HOST': '127.0.0.1',
        'POST': '5432'
    }
}

DEBUG = True