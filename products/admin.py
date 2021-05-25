from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin): # Dictates how the admin site looks and displays data. See: https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
    list_display = (
        'sku', 
        'name',
        'category',
        'price',
        'rating',
        'image',
    )
    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name'
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)