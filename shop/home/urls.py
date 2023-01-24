from django.urls import path
from home.views import Home, about, logout_user, ShowProduct, ShowCategory, AddProduct, RegisterUser, LoginUser,\
    ShowCart, add_product_cart, remove_product_cart, AddPhoto

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', about, name='about'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('add_product_photo/', AddPhoto.as_view(), name='add_product_photo'),
    path('login/', LoginUser.as_view(), name='login'),
    path('auth/', RegisterUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout'),
    path('category/<slug:category_slug>/', ShowCategory.as_view(), name='category'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
    path('cart/<int:cart_pk>/', ShowCart.as_view(), name='cart'),
    path('add_product_cart/<slug:product_slug>', add_product_cart, name='add_product_cart'),
    path('remove_product_cart/<slug:product_slug>', remove_product_cart, name='remove_product_cart')
]
