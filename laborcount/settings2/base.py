import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')


DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # Используем только один класс
            'filename': 'django.log',
            'when': 'midnight',  # ротация каждый день
            'backupCount': 7,    # хранить 7 дней логов
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',  # Уровень DEBUG для консоли
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
          'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',  # Понижаем уровень до DEBUG, чтобы видеть больше сообщений
            'propagate': True,
        },
        'main': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


ALLOWED_HOSTS = ["*"]
if DEBUG:
    print("Приложение запущено в режиме разработки 🚀")
    
    
else:
    print("Приложение запущено в рабочей версии 🤖")
       

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'laborcount.urls'




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'laborcount.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Samara'

USE_I18N = True

USE_TZ = True




STATIC_URL = '/static/'  # Обязательная настройка
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Куда собирать статику


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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