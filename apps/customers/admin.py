from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'customer_type']
    list_filter = ['customer_type']
    search_fields = ['name', 'email']
