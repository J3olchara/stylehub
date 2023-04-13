# Generated by Django 3.2.15 on 2023-04-13 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20230413_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
        migrations.AlterField(
            model_name='categorybase',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
        migrations.AlterField(
            model_name='categoryextended',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
        migrations.AlterField(
            model_name='item',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
        migrations.AlterField(
            model_name='style',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
    ]