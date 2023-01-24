from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class ProductPhoto(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название фото')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография продукта'
        verbose_name_plural = 'Фотографии продуктов'

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    photo = models.ForeignKey(ProductPhoto, on_delete=models.CASCADE, related_name='product', verbose_name='Фотография')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты(-ов)'

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    def get_absolute_url_for_add_cart(self):
        """Формирование URL для добавления продукта в корзину"""
        return reverse('add_product_cart', kwargs={'product_slug': self.slug})

    def get_absolute_url_for_remove_cart(self):
        """Формирование URL для удаления продукта из корзины"""
        return reverse('remove_product_cart', kwargs={'product_slug': self.slug})


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ManyToManyField(Product, related_name='cart')

    def __str__(self):
        return self.customer.username

    def get_absolute_url(self):
        return reverse('cart', kwargs={'cart_pk': self.customer.pk})
