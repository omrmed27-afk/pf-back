from django.contrib import admin
from .models import Shipment, ShipmentProduct


class ShipmentProductInline(admin.TabularInline):
    model = ShipmentProduct
    extra = 1


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'customer', 'status', 'calculated_cost', 'created_at']
    list_filter = ['status']
    search_fields = ['tracking_number', 'customer__name']
    readonly_fields = ['tracking_number', 'actual_delivery_date']
    inlines = [ShipmentProductInline]


@admin.register(ShipmentProduct)
class ShipmentProductAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'product', 'quantity', 'unit_price']
