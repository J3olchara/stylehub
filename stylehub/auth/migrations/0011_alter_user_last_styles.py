# Generated by Django 3.2.15 on 2023-04-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0018_item_bought'),
        ('user_auth', '0010_auto_20230415_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_styles',
            field=models.ManyToManyField(blank=True, related_name='styles', to='market.Style', verbose_name='последние пять посещённых стилей'),
        ),
    ]
