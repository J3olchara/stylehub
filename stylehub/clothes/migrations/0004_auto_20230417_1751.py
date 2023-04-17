# Generated by Django 3.2.15 on 2023-04-17 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_cart'),
        ('core', '0001_initial'),
        ('clothes', '0003_auto_20230416_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(help_text='указывает на категорию, к которой относится товар', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_category', to='market.categoryextended', verbose_name='категория товара'),
        ),
        migrations.AlterField(
            model_name='item',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.image', verbose_name='основная картинка товара'),
        ),
    ]