# Generated by Django 3.2.15 on 2023-04-16 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='designer',
            field=models.ForeignKey(help_text='какому дизайнеру принадлежит сообщение', on_delete=django.db.models.deletion.CASCADE, related_name='designers_messgaes', to=settings.AUTH_USER_MODEL, verbose_name='дизайнер отправивший сообщение'),
        ),
        migrations.AddField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(help_text='какому пользователю принадлежит сообщение', on_delete=django.db.models.deletion.CASCADE, related_name='users_messages', to=settings.AUTH_USER_MODEL, verbose_name='пользователь отправивший сообщение'),
        ),
    ]
