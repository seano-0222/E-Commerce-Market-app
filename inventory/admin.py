from django.contrib import admin
from .models import Warehouse, Inventory


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 0


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'capacity')
    search_fields = ('name', 'location')
    inlines = [InventoryInline]


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'warehouse', 'stock_level', 'reorder_threshold', 'needs_reorder', 'last_updated')
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'warehouse__name')

    @admin.display(boolean=True, description='Needs Reorder')
    def needs_reorder(self, obj):
        return obj.needs_reorder
