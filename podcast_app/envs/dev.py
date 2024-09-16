from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print('Mode : Dev')

STATIC_URL = '/api_podcast_app/api/static/'
MEDIA_URL = '/api_podcast_app/api/media/'
# Rest settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER':
        'podcast_app.config.exception_handler.CustomExceptionHandler',

    'DEFAULT_RENDERER_CLASSES': ['podcast_app.config.renderers.CustomJSONRenderer'],

}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
