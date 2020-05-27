# -*- coding: utf-8; -*-
"""
Django settings for pharmaship project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERDATA_DIR = Path.home() / ".pharmaship"
USERDATA_DIR.mkdir(parents=True, exist_ok=True)

# Pharmaship configuration
PHARMASHIP_DATA = Path(BASE_DIR) / "data"
PHARMASHIP_GUI = Path(BASE_DIR) / "gui/templates"
PHARMASHIP_REPORTS = Path(BASE_DIR) / "gui/reports"
PHARMASHIP_LOCALE = Path(BASE_DIR) / "gui/locale"
PHARMASHIP_CONF = USERDATA_DIR / "config.yaml"
PHARMASHIP_LOG = USERDATA_DIR / 'pharmaship.log'

VALIDATOR_PATH = Path(BASE_DIR) / "schemas"

PICTURES_FOLDER = USERDATA_DIR / "pictures"
PICTURES_FOLDER.mkdir(parents=True, exist_ok=True)
KEYRING_PATH = USERDATA_DIR / "keyring"
KEYRING_PATH.mkdir(parents=True, exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j5pnlald0385jm6xjxfs--fkgs8qg&^zp!g-@&xszpc2v*_(nn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third parties apps
    'rest_framework',
    'generic_relations',
    'mptt',
    # Pharmaship apps
    'pharmaship.core',
    'pharmaship.gui',
    'pharmaship.settings',
    'pharmaship.inventory',
    'pharmaship.purchase'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pharmaship.app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PHARMASHIP_REPORTS,
        ],
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


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(USERDATA_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('fr', "Français"),
    ('en', "English"),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
MEDIA_ROOT = PICTURES_FOLDER
