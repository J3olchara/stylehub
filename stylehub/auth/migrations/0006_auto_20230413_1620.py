# Generated by Django 3.2.15 on 2023-04-13 13:20

import auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_auto_20230413_1620'),
        ('user_auth', '0005_alter_user_last_styles'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', auth.models.UserManager()),
            ],
        ),
        migrations.RenameField(
            model_name='designerprofile',
            old_name='backgroound',
            new_name='background',
        ),
        migrations.AddField(
            model_name='user',
            name='cart',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='market.cart', verbose_name='корзина пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Мужской', 1), ('Женский', 0)], help_text='Укажите ваш пол', max_length=127, null=True, verbose_name='пол'),
        ),
        migrations.AlterField(
            model_name='designerprofile',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='баланс дизайнера'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
