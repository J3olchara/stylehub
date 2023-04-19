# Generated by Django 3.2.15 on 2023-04-19 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempicture',
            name='item',
            field=models.ForeignKey(help_text='добавьте как можно болеее информативные фотографии', on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='clothes.item', verbose_name='галерея изображений товара'),
        ),
    ]
