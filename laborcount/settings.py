import os
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

if(DEBUG):
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ["ep-tight-sun-a81gunnv.eastus2.azure.neon.tech","*"]


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
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PGDATABASE') or 'labor',
        'USER': os.getenv('PGUSER') or 'postgres',
        'PASSWORD': os.getenv('PGPASSWORD') or '123',  # Ensure a default empty string if not set
        'HOST': os.getenv('PG_HOST') or 'db',  # Default to localhost if not set
        'PORT': 5432,  # Default to 5432 if not set
    }
}
CACHES = {
    # we use "default" as the alias.
    "default": {
        # Here, we're using the database-backed cache backend.
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",

        # Provide a LOCATION parameter to specify the database table name where cached data will be stored.
        "LOCATION": "cached_data",
    }
}
print(DATABASES,)
# Application definition

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
