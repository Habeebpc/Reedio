from decouple import config

print('Mode: Local')

# Rest settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    # 'EXCEPTION_HANDLER':
    #     'tech_plotz.config.exception_handler.CustomExceptionHandler',

    'DEFAULT_RENDERER_CLASSES': ['tech_plotz.config.renderers.CustomJSONRenderer'],

}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DATABASE_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
