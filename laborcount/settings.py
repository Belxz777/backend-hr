import os
from pathlib import Path
from urllib.parse import urlparse
import dj_database_url
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')


DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
# settings.py

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
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',  # ротация каждый день
            'backupCount': 7,    # хранить 7 дней логов
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'myapp': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    print("Приложение запущено в режиме разработки 🚀")
    
    
else:
    ALLOWED_HOSTS = ["*"]
    print("Приложение запущено в рабочей версии 🤖")
        
use_db_url = os.getenv('IS_URL', '').lower() in ('true', '1', 'yes')

if use_db_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL') , 
            conn_max_age=600
        )
    }
else:
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

# Настройки WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": os.getenv("REDIS_URL", "redis://:belx001%2322@hr_redis:6379/0"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "SOCKET_CONNECT_TIMEOUT": 5,
#             "SOCKET_TIMEOUT": 5,
#         },
#         "KEY_PREFIX": "django_"
#     }
# }
# CACHES = { кеширование на основе файлов , медленее но без отдельных сервисов
#     # we use "default" as the alias.
#     "default": {
#         # Here, we're using the file-based cache backend.
#         "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",

#         # LOCATION parameter to specify the file system path where cached data will be stored.
#         "LOCATION": "/var/tmp/django_cache",
#     }
# }

