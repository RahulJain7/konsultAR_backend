
from djongo import models
from django.contrib.auth import get_user_model



# Create your models here.

User = get_user_model()


class AppUser(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField( max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=(('online','online'),('offline','offline')),default='offline')
    role = models.CharField(max_length=255,choices=(('technician','technician'),('expert','expert')),default='technician')
    fcmid = models.CharField(max_length=255, blank=True, null=True)
    ar_session_id = models.CharField(max_length=500, blank=True, null=True)
    ar_token = models.CharField(max_length=500, blank=True, null=True)
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='app_users'
    )

    objects = models.DjongoManager()
