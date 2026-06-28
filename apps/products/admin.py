from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'unit_price', 'stock', 'supplier']
    list_filter = ['supplier']
    search_fields = ['name', 'sku']
    list_editable = ['unit_price', 'stock']
