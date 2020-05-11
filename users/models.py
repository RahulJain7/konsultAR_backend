



import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from djongo import models
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # bp_id = models.CharField(_('external id'), max_length=255, null=True, blank=True)
    email = models.EmailField(_("Email Id"), max_length=255, unique=True)
    mobile = models.CharField(_("Mobile Number"), max_length=20, null=True, blank=True)
    first_name = models.CharField(_("First Name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True, null=True)
    is_active = models.BooleanField(_("is active"), default=True)  # can login
    is_staff = models.BooleanField(_("is staff"), default=False)  # staff user non superuser
    is_admin = models.BooleanField(_("is admin"), default=False)  # superuser
    is_online = models.BooleanField(_("is onilne"), default=False)
    
    

    USERNAME_FIELD = 'email'  # username

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"id": self.id})

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name



# Create your models here.
