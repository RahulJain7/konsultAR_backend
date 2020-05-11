from django.urls import path, re_path
from users.api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = 'users_api'

urlpatterns = [
    re_path(r'^login/$', TokenObtainPairView.as_view(), name='login'),
    re_path(r'^login/jwt/$', views.LoginView.as_view(), name='login-jwt'),
    re_path(r'^register/$', views.UserRegisterView().as_view(), name='register-user'),
]
