from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'phone', 'status']
    list_filter = ['status']
    search_fields = ['license_number', 'user__username']
