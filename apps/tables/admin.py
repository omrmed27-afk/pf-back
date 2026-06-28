from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['warehouse', 'number', 'capacity', 'status']
    list_filter = ['status', 'warehouse']
    list_editable = ['status']
