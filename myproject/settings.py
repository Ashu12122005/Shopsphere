"""
Django settings for myproject project.
Local Development Ready
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# SECURITY
# ==================================================

SECRET_KEY = "django-insecure-local-development-key"

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


CSRF_TRUSTED_ORIGINS = []


# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'base',
    'authen',
]


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==================================================
# URLS / TEMPLATES
# ==================================================

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# ==================================================
# DATABASE
# ==================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = []


# ==================================================
# LANGUAGE / TIME
# ==================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True
USE_TZ = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'


# ==================================================
# MEDIA FILES
# ==================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==================================================
# LOGIN REDIRECTS
# ==================================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# ==================================================
# JAZZMIN
# ==================================================

JAZZMIN_SETTINGS = {
    "site_title": "ShopSphere Admin",
    "site_header": "ShopSphere",
    "site_brand": "ShopSphere Dashboard",
    "welcome_sign": "Welcome to ShopSphere Admin",
    "copyright": "Ashutosh Bhanja",
    "show_sidebar": True,
    "navigation_expanded": True,

    "icons": {
        "auth.User": "fas fa-user",
        "base.Products": "fas fa-box",
        "base.CartModel": "fas fa-shopping-cart",
        "base.Order": "fas fa-truck",
    },
}


# ==================================================
# PAYMENT KEYS
# ==================================================

RAZORPAY_KEY_ID = ""
RAZORPAY_KEY_SECRET = ""