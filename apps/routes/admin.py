from django.contrib import admin
from .models import Route, RouteStop


class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1
    ordering = ['stop_order']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'origin_warehouse']
    search_fields = ['name']
    inlines = [RouteStopInline]
