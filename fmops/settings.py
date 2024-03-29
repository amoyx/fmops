"""
Django settings for fmops project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import djcelery
from celery import Celery, platforms


try:
    import ConfigParser as conf
except ImportError as e:
    import configparser as conf


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = conf.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config/ops.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v515k(st3^o1wo46b^(rgpf2yb#37sl4qqb3$4&ifj00&q8_ez'

# SECURITY WARNING: don't run with debug turned on in production!
if config.get('others', 'debug').lower() == 'false':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.assets',
    'apps.api',
    'apps.koderover',
    'apps.orders',
    'rest_framework',
    'rest_framework.authtoken',
    'djcelery'
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

ROOT_URLCONF = 'fmops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates"],
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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}


WSGI_APPLICATION = 'fmops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if config.get('db', 'engine').lower() == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config.get('db', 'database'),
            'USER': config.get('db', 'user'),
            'PASSWORD': config.get('db', 'password'),
            'HOST': config.get('db', 'host'),
            'PORT': config.getint('db', 'port'),
        }
    }
elif str(config.get('db', 'engine')).lower() == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config.get('db', 'database'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

JENKINS_HOST = config.get('jenkins', 'host')
JENKINS_USER = config.get('jenkins', 'user')
JENKINS_TOKEN = config.get('jenkins', 'token')

KODEROVER_HOST = config.get('koderover', 'host')
KODEROVER_TOKEN = config.get('koderover', 'token')

K8S_HOST = config.get('k8s', 'host')
K8S_TOKEN = config.get('k8s', 'token')

KUBERNETES_API = config.get('kubernetes', 'host')
GITLAB_PATH = config.get('gitlab', 'host')
DEPLOY_PLATFORM_HOST = config.get('fm-platform', 'host')

TENCENT_SECRET_ID=config.get('tencentcloud', 'SecretId')
TENCENT_SECRET_KEY=config.get('tencentcloud', 'SecretKey')

djcelery.setup_loader()
BROKER_URL = 'redis://:' + config.get('redis', 'password') + "@" + config.get('redis', 'host') + ":" + config.get('redis', 'port') + '/' + config.get('redis', 'db')
CELERY_RESULT_BACKEND = 'redis://:' + config.get('redis', 'password') + "@" + config.get('redis', 'host') + ":" + config.get('redis', 'port') + '/6'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle','json']
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERYD_MAX_TASKS_PER_CHILD = 500
CELERY_TRACK_STARTED = True
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'
platforms.C_FORCE_ROOT = True

CELERY = Celery(__file__, broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
