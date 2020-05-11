import datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .main import SIMPLE_JWT

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    ACCESS_TOKEN_LIFETIME = SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
    # expire = timezone.now() + ACCESS_TOKEN_LIFETIME + datetime.timedelta(hours=6)
    expire = refresh.get('exp')

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'expire': expire
    }
