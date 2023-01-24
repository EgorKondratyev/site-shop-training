# Generated by Django 4.1.5 on 2023-01-11 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название фотографии')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Фотография продукта',
                'verbose_name_plural': 'Фотографии продуктов',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('slug', models.SlugField(max_length=255, verbose_name='URL')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='home.category', verbose_name='Категория')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='home.productphoto', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты(-ов)',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
                ('product', models.ManyToManyField(related_name='cart', to='home.product')),
            ],
        ),
    ]