# Generated by Django 3.2.15 on 2023-04-13 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0004_auto_20230413_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCustom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_price', models.IntegerField(help_text='Бюджет пользователя', verbose_name='максимальная сумма заказа')),
                ('header', models.CharField(help_text='Заголовок заказа', max_length=100, verbose_name='заголовок')),
                ('text', models.TextField(blank=True, help_text='Опишите стиль, добавьте интересные факты', null=True, verbose_name='описание стиля')),
                ('status', models.CharField(choices=[('wait', 'в обработке'), ('got', 'принят'), ('proc', 'в процессе'), ('deli', 'в доставке'), ('done', 'выполнен')], default='wait', help_text='Заголовок заказа', max_length=4, verbose_name='заголовок')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Автоматически выставляется при создании', verbose_name='дата и время создания')),
                ('edited', models.DateTimeField(auto_now=True, help_text='Автоматически выставляется при изменении объекта', verbose_name='дата и время последнего редактирования')),
                ('designer', models.ForeignKey(help_text='Дизайнер, получивший заказ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='designer', to=settings.AUTH_USER_MODEL, verbose_name='дизайнер')),
                ('user', models.ForeignKey(help_text='Пользователь, оформивший заказ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='заказчик')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(help_text='Изображение желаемого дизайна', upload_to='media/uploads/order_pictures', verbose_name='изображение')),
                ('order', models.ForeignKey(help_text='Номер заказа', on_delete=django.db.models.deletion.CASCADE, to='market.ordercustom', verbose_name='заказ')),
            ],
        ),
    ]
