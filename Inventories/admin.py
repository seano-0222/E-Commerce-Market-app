from django.contrib import admin
from .models import Inventory, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouse_id', 'name', 'location', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'inventory_id', 'product', 'warehouse',
        'quantity', 'reorder_threshold', 'is_low_stock',
    )
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'warehouse__name')
    readonly_fields = ('created_at', 'updated_at')
