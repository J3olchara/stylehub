# Generated by Django 3.2.15 on 2023-04-12 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_auto_20230412_0037'),
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
                ('main_image', models.ImageField(blank=True, null=True, upload_to='items/main_images', verbose_name='основная картинка товара')),
                ('cost', models.PositiveBigIntegerField(help_text='добавьте стоимость вашего товара', verbose_name='стоимость товара')),
                ('text', models.TextField(blank=True, help_text='опишите ваш товар', null=True, verbose_name='описание товара')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Автоматически выставляется при создании', verbose_name='время добавления на сайт')),
                ('edited', models.DateTimeField(auto_now=True, help_text='Автоматически выставляется при изменении объекта', verbose_name='время и дата последнего изменения товара')),
                ('category', models.ForeignKey(help_text='указывает на категорию, к которой относится товар', on_delete=django.db.models.deletion.CASCADE, to='market.categoryextended', verbose_name='категория товара')),
                ('collection', models.ManyToManyField(help_text='показывает участвует ли товар в каких-либо коллекциях', to='market.Collection', verbose_name='коллекции, в которых есть этот товар')),
                ('designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth.designer')),
                ('styles', models.ManyToManyField(help_text='указывает к какому стилю принадлежит товар', to='market.Style', verbose_name='стиль товара')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='', verbose_name='изображение')),
                ('item', models.ManyToManyField(help_text='добавьте как можно болеее информативные фотографии', to='market.Item', verbose_name='галерея изображений товара')),
            ],
        ),
    ]