# Generated by Django 2.2.9 on 2020-05-08 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0002_appuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='status',
            field=models.CharField(choices=[('online', 'online'), ('offline', 'offline')], default='offline', max_length=255),
        ),
    ]
