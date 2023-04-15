# Generated by Django 3.2.15 on 2023-04-15 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0014_item_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='collection',
            field=models.ForeignKey(help_text='показывает участвует ли товар в каких-либо коллекциях', on_delete=django.db.models.deletion.CASCADE, to='market.collection', verbose_name='коллекция, в которой есть этот товар'),
        ),
        migrations.AlterField(
            model_name='ordercustom',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Когда объект был создан', verbose_name='дата и время создания'),
        ),
        migrations.AlterField(
            model_name='ordercustom',
            name='edited',
            field=models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования'),
        ),
    ]
