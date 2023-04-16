# Generated by Django 3.2.15 on 2023-04-16 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('custom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercustom',
            name='designer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_custom_designer', to=settings.AUTH_USER_MODEL, verbose_name='исполнитель'),
        ),
        migrations.AddField(
            model_name='ordercustom',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_custom_user', to=settings.AUTH_USER_MODEL, verbose_name='заказчик'),
        ),
    ]
