# Generated by Django 3.2.15 on 2023-04-18 09:56

import auth.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_auto_20230416_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, verbose_name='Ключ активации')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('expire', models.DateTimeField(default=auth.utils.get_token_expire, verbose_name='Дата и время истечения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
