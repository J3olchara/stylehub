# Generated by Django 3.2.15 on 2023-04-19 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0006_rename_failed_attempls_activationtoken_failed_attemps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activationtoken',
            name='failed_attemps',
        ),
        migrations.AddField(
            model_name='user',
            name='failed_attemps',
            field=models.IntegerField(default=0, verbose_name='Неудачных попыток входа'),
        ),
    ]
