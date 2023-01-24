from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Sum

from home.models import Product, Cart
from home.form import AddProductForm, CustomUserCreationForm, AddProductPhotoForm
from home.utils import DataMixin


class Home(DataMixin, ListView):
    model = Product
    template_name = 'home/home.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(Home, self).get_context_data()
        context = self.user_context_data(**context_base)
        return context


class ShowCategory(DataMixin, ListView):
    model = Product
    template_name = 'home/home.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(ShowCategory, self).get_context_data()
        context = self.user_context_data(**context_base)
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


class ShowCart(DataMixin, ListView):
    model = Product
    template_name = 'home/cart.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(ShowCart, self).get_context_data()
        price = context_base['products'].aggregate(sum=Sum('price'))
        context = self.user_context_data(**context_base, price=price)
        return context

    def get_queryset(self):
        return Product.objects.filter(cart__customer__pk=self.kwargs['cart_pk'])


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = 'home/post.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(ShowProduct, self).get_context_data()
        # check_product_in_cart_user - проверяет есть ли продукт в корзине пользователя.
        check_product_in_cart_user = 2
        if self.request.user.is_authenticated:
            check_product_in_cart_user = bool(self.request.user.cart.product.filter(name=context_base['product'].name))
        context = self.user_context_data(**context_base, title=context_base['product'].name,
                                         check_product_in_cart_user=check_product_in_cart_user)
        return context


class AddProduct(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddProductForm
    template_name = 'home/addproduct.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(AddProduct, self).get_context_data()
        context = self.user_context_data(**context_base, title='Добавление нового товара')
        return context


class AddPhoto(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddProductPhotoForm
    template_name = 'home/add_product_photo.html'
    success_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(AddPhoto, self).get_context_data()
        context = self.user_context_data(**context_base, title='Добавление новой фотографии для товара')
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'home/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(RegisterUser, self).get_context_data()
        context = self.user_context_data(**context_base, title='Регистрация')
        return context

    def form_valid(self, form):
        user = form.save()
        Cart.objects.create(customer=user)
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'home/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_base = super(LoginUser, self).get_context_data()
        context = self.user_context_data(**context_base, title='Регистрация')
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def add_product_cart(request, product_slug):
    cart = Cart.objects.get(customer__pk=request.user.pk)
    product = Product.objects.get(slug=product_slug)
    cart.product.add(product)
    return redirect('home')


def remove_product_cart(request, product_slug):
    cart = Cart.objects.get(customer__pk=request.user.pk)
    product = Product.objects.get(slug=product_slug)
    cart.product.remove(product)
    return redirect('home')


def about(request):
    return HttpResponse('123')


def logout_user(request):
    logout(request)
    return redirect('home')


def get_category(request, category_slug):
    return HttpResponse('123 category')
