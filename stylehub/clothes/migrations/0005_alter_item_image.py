# Generated by Django 3.2.15 on 2023-04-19 21:14

from django.db import migrations, models
import utils.functions


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0004_alter_itempicture_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='defaults/item.png', help_text='Загрузите фото', max_length=255, null=True, upload_to=utils.functions.get_image_upload_location, verbose_name='обложка'),
        ),
    ]
