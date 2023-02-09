from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from home.models import Category, Cart


# Последовательность имеет значение
menu = [
    {'title': 'Домашняя страница', 'url_name': 'home'},  # 0
    {'title': 'О сайте', 'url_name': 'about'},  # 1
    {'title': 'Добавить товар', 'url_name': 'add_product'},  # 2
    {'title': 'Добавить фото товара', 'url_name': 'add_product_photo'}  # 3
]


class DataMixin:
    paginate_by = 6

    def user_context_data(self, **kwargs):
        context = kwargs
        menu_context = menu.copy()
        if not self.request.user.is_authenticated:
            menu_context.pop(3)
            menu_context.pop(2)
        else:
            try:
                context['cart'] = Cart.objects.get(customer__pk=self.request.user.pk)
            except ObjectDoesNotExist:
                Cart.objects.create(customer=self.request.user)
                context['cart'] = Cart.objects.get(customer__pk=self.request.user.pk)

        context['menu'] = menu_context

        if not context.get('title'):
            context['title'] = 'Страница'

        if not context.get('category_selected'):
            context['category_selected'] = 0

        context['categories'] = Category.objects.annotate(total=Count('product')).filter(total__gte=1)
        return context
