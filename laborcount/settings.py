import os
from pathlib import Path
from urllib.parse import urlparse
import dj_database_url
from dotenv import load_dotenv
import psycopg2
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    print("Приложение запущено в debug mode")
else:
    ALLOWED_HOSTS = ["*"]#specify certain
    print("Приложение запущено в production mode")


# Database connection
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'main_agry',
#         'USER': 'postgres1',
#         'PASSWORD': 'awpbMho0QStEeHfPUl96bY0ApIEnoBOm' ,  # Ensure a default empty string if not set
#         'HOST': 'dpg-cti3fnogph6c73d4kekg-a.frankfurt-postgres.render.com',  # Default to localhost if not set
#         'PORT': os.getenv('PGPORT') or 5432,  # Default to 5432 if not set
#     }
# }  
    # DATABASES = {
    # 'default': dj_database_url.config(
    #     # Replace this value with your local database's connection string.        default='postgresql://postgres:postgres@localhost:5432/mysite',        conn_max_age=600    
        
    #     )
    #     }
# DATABASES = { 
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('PGDATABASE') or 'labor',
#         'USER': os.getenv('PGUSER') or 'postgres',
#         'PASSWORD': os.getenv('PGPASSWORD') or '123',  # Ensure a default empty string if not set
#         'HOST': os.getenv('PG_HOST') or 'localhost',  # Default to localhost if not set
#         'PORT': 5432, 
#     }
# }
# try:
#     conn = psycopg2.connect(
#         dbname="test_pyco",
#         user="test_pyco_user",
#         password="zhsN9ck24KHRfx8JVVvGESCAwooM0Civ",
#         host="dpg-cuhl54jtq21c73bbpai0-a",
#         port=5432
#     )
#     print("Connection successful!")
#     conn.close()
# except Exception as e:
#     print(f"Connection failed: {e}")
# Replace the SQLite DATABASES configuration with PostgreSQL:
# connection for render database external via url
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default=os.getenv('DATABASE_URL') or 'postgresql://test_pyco_user:zhsN9ck24KHRfx8JVVvGESCAwooM0Civ@dpg-cuhl54jtq21c73bbpai0-a.frankfurt-postgres.render.com/test_pyco',
        conn_max_age=600
    )
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
    'rest_framework_swagger',
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
