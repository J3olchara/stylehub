# Generated by Django 3.2.15 on 2023-04-12 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.functions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Придумайте название', max_length=50, verbose_name='название')),
                ('slug', models.SlugField(help_text='Нормализованное имя', unique=True, verbose_name='слаг')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Автоматически выставляется при создании', verbose_name='дата и время создания')),
                ('edited', models.DateTimeField(auto_now=True, help_text='Автоматически выставляется при изменении объекта', verbose_name='дата и время последнего редактирования')),
                ('text', models.TextField(verbose_name='описание коллекции')),
                ('designer', models.ForeignKey(help_text='Укажите кто создал эту коллекцию', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='дизайнер коллекции')),
                ('style', models.ManyToManyField(to='market.Style', verbose_name='стиль коллекции')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Придумайте название', max_length=50, verbose_name='название')),
                ('slug', models.SlugField(help_text='Нормализованное имя', unique=True, verbose_name='слаг')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Автоматически выставляется при создании', verbose_name='дата и время создания')),
                ('edited', models.DateTimeField(auto_now=True, help_text='Автоматически выставляется при изменении объекта', verbose_name='дата и время последнего редактирования')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=utils.functions.get_item_main_image_location, verbose_name='основная картинка товара')),
                ('cost', models.PositiveBigIntegerField(help_text='добавьте стоимость вашего товара', verbose_name='стоимость товара')),
                ('text', models.TextField(blank=True, help_text='опишите ваш товар', null=True, verbose_name='описание товара')),
                ('category', models.ForeignKey(help_text='указывает на категорию, к которой относится товар', on_delete=django.db.models.deletion.CASCADE, to='market.categoryextended', verbose_name='категория товара')),
                ('collection', models.ForeignKey(help_text='показывает участвует ли товар в каких-либо коллекциях', on_delete=django.db.models.deletion.CASCADE, to='market.collection', verbose_name='коллекции, в которых есть этот товар')),
                ('designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('styles', models.ManyToManyField(help_text='указывает к какому стилю принадлежит товар', to='market.Style', verbose_name='стиль товара')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='', verbose_name='изображение')),
                ('item', models.ForeignKey(help_text='добавьте как можно болеее информативные фотографии', on_delete=django.db.models.deletion.CASCADE, to='market.item', verbose_name='галерея изображений товара')),
            ],
        ),
    ]
