from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print('Mode : Dev')

STATIC_URL = '/api_boilerplate/api/static/'
MEDIA_URL = '/api_boilerplate/api/media/'
# Rest settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER':
        'boilerplate.config.exception_handler.CustomExceptionHandler',

    'DEFAULT_RENDERER_CLASSES': ['boilerplate.config.renderers.CustomJSONRenderer'],

}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
