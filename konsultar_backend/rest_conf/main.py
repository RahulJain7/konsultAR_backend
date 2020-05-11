from datetime import timedelta
import environ

env = environ.Env()

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'config.rest_conf.pagination.StandardOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'SEARCH_PARAM': 'q',
    'ORDERING_PARAM': 'ordering',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    #'SIGNING_KEY': env("DJANGO_SECRET_KEY"),
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=6),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


JWT_AUTH = {
   # 'JWT_SECRET_KEY': env("DJANGO_SECRET_KEY"),
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_payload',
    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_token',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'rest_framework_jwt.utils.jwt_get_username_from_payload_handler',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': timedelta(seconds=24*3600),    # 24 hours
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'konsultar.users.utils.jwt_response_payload_handler',
        # 'rest_framework_jwt.utils.jwt_create_response_payload',
    'JWT_AUTH_COOKIE': None
}


REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'rest_auth.serializers.LoginSerializer',
    'JWT_SERIALIZER': 'konsultar.users.api.serializers.JWTSerializer',
    'PASSWORD_RESET_SERIALIZER': 'rest_auth.serializers.PasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'rest_auth.serializers.PasswordResetConfirmSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'rest_auth.serializers.PasswordChangeSerializer',
    'USER_DETAILS_SERIALIZER': 'konsultar.users.api.serializers.CustomUserDetailsSerializer'
}
