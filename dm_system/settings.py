"""
Django settings for dm_system project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# print(f"SECRET_KEY: {SECRET_KEY}")
# print(f"DEBUG: {DEBUG}")
# print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # mine
    'auth_app', 
    'customer_app', 
    'django_celery_results', 
    'django_celery_beat',
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

ROOT_URLCONF = 'dm_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR / 'templates')],
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

WSGI_APPLICATION = 'dm_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "mydatabase",
#         "USER": "mydatabaseuser",
#         "PASSWORD": "mypassword",
#         "HOST": "127.0.0.1",
#         "PORT": "3306",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'isolation_level': 'read committed',
        },
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# updated the static and media
STATIC_URL = 'static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#AbstractBaseUser
AUTH_USER_MODEL = "auth_app.User"


# # CELERY SETTINGS
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Kolkata'

# CELERY_RESULT_BACKEND = 'django-db'

# #CELERY BEAT
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# SMTP Settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'mail.weamse.dev'
# EMAIL_PORT = 587  # Use 465 for SSL or 587 for TLS
# EMAIL_USE_TLS = True  # Use False if using SSL
# EMAIL_HOST_USER = 'noreply@weamse.dev'
# EMAIL_HOST_PASSWORD = '+;7D1.Ue#[=,'
# DEFAULT_FROM_EMAIL = 'noreply@weamse.dev'


# CELERY SETTINGS
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = env.list('CELERY_ACCEPT_CONTENT')
CELERY_RESULT_SERIALIZER = env('CELERY_RESULT_SERIALIZER')
CELERY_TASK_SERIALIZER = env('CELERY_TASK_SERIALIZER')
CELERY_TIMEZONE = env('CELERY_TIMEZONE')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

# print(f"CELERY_BROKER_URL: {CELERY_BROKER_URL}")
# print(f"CELERY_ACCEPT_CONTENT: {CELERY_ACCEPT_CONTENT}")
# print(f"CELERY_RESULT_SERIALIZER: {CELERY_RESULT_SERIALIZER}")
# print(f"CELERY_TASK_SERIALIZER: {CELERY_TASK_SERIALIZER}")
# print(f"CELERY_TIMEZONE: {CELERY_TIMEZONE}")
# print(f"CELERY_RESULT_BACKEND: {CELERY_RESULT_BACKEND}")

# CELERY BEAT
CELERY_BEAT_SCHEDULER = env('CELERY_BEAT_SCHEDULER')

# Print CELERY BEAT setting
# print(f"CELERY_BEAT_SCHEDULER: {CELERY_BEAT_SCHEDULER}")

# for showing task result in admin celery result
# CELERY_RESULT_EXTENDED = True
CELERY_RESULT_EXTENDED = env('CELERY_RESULT_EXTENDED')

# SMTP Settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

print(f"EMAIL_BACKEND: {EMAIL_BACKEND}")
print(f"EMAIL_HOST: {EMAIL_HOST}")
print(f"EMAIL_PORT: {EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {EMAIL_HOST_PASSWORD}")
print(f"DEFAULT_FROM_EMAIL: {DEFAULT_FROM_EMAIL}")
