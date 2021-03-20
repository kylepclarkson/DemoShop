from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'featured', 'quantity', 'created', 'updated']
    list_filter = ['featured', 'quantity', 'created', 'updated']
    list_editable = ['price', 'featured', 'quantity']
    prepopulated_fields = {
        'slug': ('name',)
    }
