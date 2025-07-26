from .base import *
import os

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Исправлено: ENGINE -> ENGINE, postgresql_psycopg2
            'NAME': os.getenv('DATABASE_NAME', 'ANY'),
            'USER': os.getenv('DATABASE_USER', 'postgres'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD', 'ANY'),
            'HOST': os.getenv('DATABASE_HOST', 'localhost'),
            'PORT': os.getenv('DATABASE_PORT', '5432'),  # Лучше строку, так как порт может быть переменной окружения
        }
    }

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')


CACHES = {


    "default": {


        "BACKEND": "django_redis.cache.RedisCache",


        "LOCATION": REDIS_URL,


        "OPTIONS": {


            "CLIENT_CLASS": "django_redis.client.DefaultClient",


            "SOCKET_CONNECT_TIMEOUT": 5,


            "SOCKET_TIMEOUT": 5,


        },


        "KEY_PREFIX": "django_"


    }


}