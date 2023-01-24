from django.contrib import admin
from home.models import Product, ProductPhoto, Category


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPhoto)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)
