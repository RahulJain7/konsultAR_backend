from datetime import timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models import Q
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name=None, last_name=None,
            password=None, is_active=True, is_staff=False, is_admin=False):

        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)  # chanage user password
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_new_user(
            self, email, first_name=None, last_name=None, mobile=None,
            password=None, is_active=True, user_type=None, is_staff=False, is_admin=False):

        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            user_type=user_type,
        )
        user_obj.set_password(password)  # chanage user password
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            # user_type='staff'
        )
        return user

    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True,
            # user_type='admin'
        )
        return user

    def get_user_by_email(self, email):
        qs = self.get_queryset().filter(email=email)
        if qs.exists():
            user_obj = qs.first()
            return user_obj

    def get_or_create_new_user(self, fields):
        email = fields.get('email')
        user_obj = self.get_user_by_email(email)
        if user_obj:
            return user_obj, False
        else:
            user_obj = self.create_new_user(**fields)
            return user_obj, True

