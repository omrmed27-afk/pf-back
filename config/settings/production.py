from .base import *
from decouple import config
import urllib.parse

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',') if s.strip()])

RAILWAY_DOMAIN = config('RAILWAY_PUBLIC_DOMAIN', default='')
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)
    CSRF_TRUSTED_ORIGINS = [f'https://{RAILWAY_DOMAIN}']

_db_url = config('DATABASE_URL', default='')
if _db_url:
    _parsed = urllib.parse.urlparse(_db_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': _parsed.path[1:],
            'USER': _parsed.username,
            'PASSWORD': _parsed.password,
            'HOST': _parsed.hostname,
            'PORT': _parsed.port or 5432,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('PGDATABASE', default=config('DB_NAME', default='')),
            'USER': config('PGUSER', default=config('DB_USER', default='')),
            'PASSWORD': config('PGPASSWORD', default=config('DB_PASSWORD', default='')),
            'HOST': config('PGHOST', default=config('DB_HOST', default='')),
            'PORT': config('PGPORT', default=config('DB_PORT', default='5432')),
        }
    }

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
