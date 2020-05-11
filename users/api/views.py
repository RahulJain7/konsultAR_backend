from konsultar_backend.rest_conf.utils import get_tokens_for_user
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import AnonPermissionOnly
from .serializers import (
    LoginResponseSerializer,
    LoginSerializer,
    UserRegisterSerializer,
    MyTokenObtainPairSerializer,
)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AuthAPIView(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'error': 'You are already authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        if not request.data:
            return Response({'error': "Please provide email/password"}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email')  # email address
        password = data.get('password')

        qs = User.objects.filter(
            Q(email__iexact=email)
        ).distinct()
        if qs:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                if not user.is_active:
                    return Response({"error": "Inactive Account"}, status=status.HTTP_400_BAD_REQUEST)

                response = {
                    'email': user_obj.email,
                    'first_name': user_obj.first_name,
                    'last_name': user_obj.last_name,
                    'last_login': user_obj.last_login,
                    'token': get_tokens_for_user(user)
                }
                print('here')
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(response, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    permission_classes = [AnonPermissionOnly]
    serializer_class = LoginSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {
            "request": self.request,
            "args": self.args,
            "kwargs": self.kwargs
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer_class = LoginResponseSerializer
        user = serializer.validated_data.get('user')
        response_serializer = serializer_class(instance=user, context={'request': self.request})
        response = Response(response_serializer.data, status=status.HTTP_200_OK)
        return response


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {
            "request": self.request,
            "args": self.args,
            "kwargs": self.kwargs
        }
