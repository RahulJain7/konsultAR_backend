import datetime
from django.utils import timezone
from collections import namedtuple
from rest_framework_jwt.settings import api_settings


def jwt_response_payload_handler(token, user=None, request=None):
    EXPIRE_DELTA = api_settings.JWT_REFRESH_EXPIRATION_DELTA
    return {
        'token': token,
        'expire': timezone.now() + EXPIRE_DELTA - datetime.timedelta(
            seconds=24 * 3600),  # 24 hours
    }


def jwt_create_response_payload(token, user=None, request=None, issued_at=None):
    """
    Return data ready to be passed to serializer.

    Override this function if you need to include any additional data for
    serializer.

    Note that we are using `pk` field here - this is for forward compatibility
    with drf add-ons that might require `pk` field in order (eg. jsonapi).
    """

    response_payload = namedtuple('ResponsePayload', 'pk token user')
    response_payload.pk = issued_at
    response_payload.token = token
    response_payload.user = user

    return response_payload
