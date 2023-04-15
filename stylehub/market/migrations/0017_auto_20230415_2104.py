# Generated by Django 3.2.15 on 2023-04-15 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0016_merge_0015_auto_20230415_1608_0015_auto_20230415_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='item',
            field=models.ForeignKey(help_text='товар, к которому оставили отзыв', on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='market.item', verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='orderclothes',
            name='status',
            field=models.CharField(choices=[('wait', 'Ожидает'), ('got', 'Принят'), ('proc', 'в процессе'), ('deli', 'доставка'), ('done', 'выполнен')], default='wait', max_length=127),
        ),
    ]
