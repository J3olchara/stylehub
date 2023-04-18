# Generated by Django 3.2.15 on 2023-04-18 15:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('custom', '0003_alter_ordercustom_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCustomEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Когда объект был создан', verbose_name='дата и время создания')),
                ('edited', models.DateTimeField(auto_now=True, help_text='Когда объект в последний раз редактировали', verbose_name='дата и время редактирования')),
                ('rating', models.PositiveSmallIntegerField(choices=[(5, 'Отличный товар'), (4, 'Хороший товар'), (3, 'Обычный товар'), (2, 'Плохой товар'), (1, 'Ужасный товар')], help_text='Ваша оценка', validators=[django.core.validators.MaxValueValidator(5, message='Максимальное значение оценки - 5'), django.core.validators.MinValueValidator(1, message='Минимальное значение оценки - 1')], verbose_name='оценка')),
                ('goods', models.TextField(blank=True, null=True, verbose_name='Достоинства')),
                ('negatives', models.TextField(blank=True, null=True, verbose_name='Недостатки')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('order', models.ForeignKey(help_text='заказ, к которому оставили отзыв', on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='custom.ordercustom', verbose_name='заказ')),
                ('user', models.ForeignKey(help_text='пользователь, оставивший отзыв', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custom_evaluations', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
    ]