"""StyleHub settings"""
import os
from pathlib import Path

import django_stubs_ext
from dotenv import load_dotenv

django_stubs_ext.monkeypatch()

BASE_DIR = Path(__file__).resolve().parent.parent

if not load_dotenv(BASE_DIR.parent / 'environs' / '.env'):
    load_dotenv(BASE_DIR.parent / 'environs' / 'example.env')
    print(
        'LOADED example.env BECAUSE YOU HAD NOT CREATED .env IN environs DIR'
    )


def get_env_bool(var_name: str) -> bool:
    """converts string variable from env to bool"""
    var = os.getenv(var_name)
    if not var:
        return False
    return var.lower() in ('y', 'yes', 't', 'true', '1')


# very important variables

SECRET_KEY = os.getenv('SECRET_KEY', 'not_secret_key')

DEBUG = get_env_bool('DJANGO_DEBUG')
ALLOWED_HOSTS = os.getenv('DJANGO_HOSTS', '').split()

AUTH_USER_MODEL = 'user_auth.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth.apps.AuthConfig',
    'chat.apps.ChatConfig',
    'clothes.apps.ClothesConfig',
    'core.apps.CoreConfig',
    'custom.apps.CustomConfig',
    'home.apps.HomeConfig',
    'market.apps.MarketConfig',
    'stats.apps.StatsConfig',
    'django_cleanup.apps.CleanupConfig',
    'sorl.thumbnail',
    'django_extensions',
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

if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.append('debug_toolbar')

ROOT_URLCONF = 'stylehub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'stylehub.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        ),
    },
]


# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static_dev/'
STATICFILES_DIRS = [BASE_DIR / 'static_dev']

# STATIC_ROOT = BASE_DIR / 'static_dev' с этим не работает

# Media files path

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Auth/Login pages

LOGIN_URL = 'admin/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# project filter variables

POPULAR_COLLECTION_BUYS = int(os.environ['POPULAR_COLLECTION_BUYS'])
POPULAR_DESIGNER_BUYS = int(os.environ['POPULAR_DESIGNER_BUYS'])
DESIGNERS_ON_CUSTOM_MAIN_PAGE = int(
    os.environ['DESIGNERS_ON_CUSTOM_MAIN_PAGE']
)
