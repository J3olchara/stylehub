# Generated by Django 3.2.15 on 2023-04-19 17:56

from django.db import migrations, models
import utils.functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Приложите свое вложение к сообщению', null=True, upload_to=utils.functions.get_message_image_upload_location, verbose_name='Приложение к сообщению')),
                ('message', models.TextField(help_text='введите текст сообщения', verbose_name='текст сообщения')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Автоматически выставляется при создании', verbose_name='дата и время создания')),
            ],
        ),
    ]
