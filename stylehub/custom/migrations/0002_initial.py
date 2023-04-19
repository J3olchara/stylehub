# Generated by Django 3.2.15 on 2023-04-19 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercustomevaluation',
            name='user',
            field=models.ForeignKey(help_text='пользователь, оставивший отзыв', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custom_evaluations', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
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
