from django.contrib import admin
from .models import Product, Discount


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('product_id', 'name', 'price', 'stock_qty', 'category')
    search_fields = ('name',)
    list_filter   = ('category',)
    ordering      = ('name',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display  = ('discount_id', 'name', 'percentage', 'start_date', 'end_date')
    search_fields = ('name',)
    filter_horizontal = ('products',)
