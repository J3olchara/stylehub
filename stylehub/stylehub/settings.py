"""StyleHub settings"""
import os
from pathlib import Path
from typing import Any, Dict, List, Union

import django_stubs_ext
from django.utils.translation import gettext_lazy as _
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
    if var is None:
        return False
    return var.lower() in ('y', 'yes', 't', 'true', '1')


# --------------------------------------------------------------------
# ------------------------Project Parameters Section------------------
# --------------------------------------------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'not_secret_key')

DEBUG = get_env_bool('DJANGO_DEBUG')
ALLOWED_HOSTS = os.getenv('DJANGO_HOSTS', '').split()

AUTH_USER_MODEL = 'user_auth.User'

SITE_EMAIL = 'help@stylehub.com'


# --------------------------------------------------------------------
# ----------------------------Apps Section----------------------------
# --------------------------------------------------------------------

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
    'api.apps.ApiConfig',
    'django_cleanup.apps.CleanupConfig',
    'sorl.thumbnail',
    'django_extensions',
]

# --------------------------------------------------------------------
# --------------------------Middleware Section------------------------
# --------------------------------------------------------------------

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

# -----------------------------------------------------------------------
# ---------------------------Templates Section---------------------------
# -----------------------------------------------------------------------

TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
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

WSGI_APPLICATION: str = 'stylehub.wsgi.application'


# -----------------------------------------------------------------------
# ----------------------------Database Section---------------------------
# -----------------------------------------------------------------------

DATABASES: Dict[str, Dict[str, Union[str, Path]]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -----------------------------------------------------------------------
# --------------------------USER AUTH Section----------------------------
# -----------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.' 'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

AUTHENTICATION_BACKENDS = ['stylehub.backends.LoginBackend']

FAILED_AUTHS_TO_DEACTIVATE = int(os.getenv('FAILED_AUTHS_TO_DEACTIVATE', '10'))

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'
LOGOUT_REDIRECT_URL = '/'

NEW_USERS_ACTIVATED = DEBUG or get_env_bool('NEW_USERS_ACTIVATED')

ACTIVATION_URL_EXPIRE_TIME = os.getenv(
    'ACTIVATION_URL_EXPIRE_TIME', '00 12:00:00'
)

# -----------------------------------------------------------------------
# -------------------------Client settings Section-----------------------
# -----------------------------------------------------------------------

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# -----------------------------------------------------------------------
# ----------------------Static/Media Files Section-----------------------
# -----------------------------------------------------------------------

STATIC_URL: str = '/static/'

STATICFILES_DIR_DEV = BASE_DIR / 'static_dev'

STATICFILES_DIRS = [
    STATICFILES_DIR_DEV,
]


MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# --------------------------------------------------------------------
# --------------------------locale Section----------------------------
# --------------------------------------------------------------------

LOCALE = 'ru'
LOCALE_FALLBACK = 'en'
LOCALES = ('ru', 'en')
LOCALES_PATH = BASE_DIR / 'locale'
LOCALE_PATHS = (BASE_DIR / 'locale',)

LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

# -----------------------------------------------------------------------
# --------------------------------EMAIL----------------------------------
# -----------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = BASE_DIR / 'send_email'


# -----------------------------------------------------------------------
# --------------------------Project variables----------------------------
# -----------------------------------------------------------------------

POPULAR_COLLECTION_BUYS = int(os.environ['POPULAR_COLLECTION_BUYS'])
POPULAR_DESIGNER_BUYS = int(os.environ['POPULAR_DESIGNER_BUYS'])
NEW_USER_IS_ACTIVE = get_env_bool('NEW_USER_IS_ACTIVE')
DESIGNERS_ON_CUSTOM_MAIN_PAGE = int(
    os.environ['DESIGNERS_ON_CUSTOM_MAIN_PAGE']
)

# -----------------------------------------------------------------------
# ------------------------------Other Section----------------------------
# -----------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
