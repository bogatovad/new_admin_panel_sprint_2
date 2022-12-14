import os
from pathlib import Path
from split_settings.tools import include
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent
config = dotenv_values(".env")
DEBUG = config.get('DEBUG', False) == 'True'

include(
    'components/database.py',
    'components/middleware.py',
    'components/auth_validators.py',
    'components/installed_apps.py',
    'components/templates.py',
)

SECRET_KEY = config.get('SECRET_KEY')
ALLOWED_HOSTS = config.get('ALLOWED_HOSTS').split(',')
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000"]

LOCALE_PATHS = ['movies/locale']

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
