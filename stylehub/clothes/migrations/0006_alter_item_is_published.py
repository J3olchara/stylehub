# Generated by Django 3.2.15 on 2023-04-21 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0005_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='опубликован?'),
        ),
    ]
