from django.contrib import admin
from .models import Transport


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'vehicle_type', 'brand', 'model', 'status']
    list_filter = ['vehicle_type', 'status']
    list_editable = ['status']
