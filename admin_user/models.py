
from djongo import models
from django.contrib.auth import get_user_model



# Create your models here.

User = get_user_model()


class AdminUser(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField( max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='admin_users'
    )

    objects = models.DjongoManager()
