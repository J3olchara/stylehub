# Generated by Django 3.2.15 on 2023-04-18 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0004_ordercustomevaluation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercustompicture',
            name='picture',
            field=models.ImageField(help_text='Изображение желаемого дизайна', upload_to='uploads/order_pictures', verbose_name='изображение'),
        ),
    ]