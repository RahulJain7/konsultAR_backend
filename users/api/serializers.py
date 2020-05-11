import logging
import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from konsultar_backend.rest_conf.utils import get_tokens_for_user
from rest_auth.utils import import_callable
import pymongo

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['ar_database']
usercol = mydb['app_users_appuser']

User = get_user_model()

logger = logging.getLogger(__name__)


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
        read_only_fields = ('email',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.first_name
        return token


class LoginResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    # expire = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'last_login',
            'token',
        ]

    def get_token(self, obj):
        token = get_tokens_for_user(obj)
        app_user = usercol.find_one({'email':obj.email})
        resp = {}
        for data in app_user:
            resp = data
        ser_resp = json.loads(json_util.dumps(resp))
        print(ser_resp)
        re = {'token':token,'profile':ser_resp}
        return re

    # def get_token(self, obj):  # instance of the model
    #     user = obj
    #     payload = jwt_payload_handler(user)
    #     user_id = payload.get('user_id')
    #     payload['user_id'] = str(user_id)
    #     token = jwt_encode_handler(payload)
    #     return token

    # def get_expire(self, obj):
    #     expiration = datetime.datetime.utcnow() + expire_delta
    #     return expiration


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)

    class Meta:
        fields = [
            'email',
            'password',
        ]

    def authenticate(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = None
        qs = User.objects.filter(
            Q(email__iexact=email)
        ).distinct()
        if qs.exists():
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                app_user = usercol.find_one({'email':email})
                resp = {}
                for data in app_user:
                    resp = data
                ser_resp = json.loads(json_util.dumps(resp))
                re = {'token':user,'profile':ser_resp}
                return re
            return user
        return user

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)
        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = self._validate_email(email, password)
        if not user:
            msg = _('Invalid credentials.')
            raise exceptions.ValidationError(msg)
        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = MyTokenObtainPairSerializer(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            'message',
            'token'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering. Please verify your email before continuing."

    def get_token(self, obj):
        token = get_tokens_for_user(obj)
        return token

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already registered")
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        user_obj = User.objects.create_new_user(**validated_data)
        return user_obj


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
        JWTUserDetailsSerializer = import_callable(
            rest_auth_serializers.get('USER_DETAILS_SERIALIZER', CustomUserDetailsSerializer)
        )
        user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
        return user_data
