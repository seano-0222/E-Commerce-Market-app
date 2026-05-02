"""
Admin configuration for the cart app.
"""

from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Show CartItems inline inside the Cart admin page."""
    model  = CartItem
    extra  = 0
    fields = ('product', 'quantity', 'get_subtotal')
    readonly_fields = ('get_subtotal',)

    @admin.display(description='Subtotal')
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display  = ('cart_id', 'get_customer_name', 'get_item_count', 'get_total', 'created_at')
    search_fields = ('customer__person__first_name', 'customer__person__last_name')
    inlines       = [CartItemInline]

    @admin.display(description='Customer')
    def get_customer_name(self, obj):
        return str(obj.customer.person)

    @admin.display(description='Items')
    def get_item_count(self, obj):
        return obj.get_item_count()

    @admin.display(description='Total')
    def get_total(self, obj):
        return f"${obj.get_total():.2f}"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display  = ('cart_item_id', 'get_customer', 'product', 'quantity', 'get_subtotal')
    search_fields = ('cart__customer__person__first_name', 'product__name')

    @admin.display(description='Customer')
    def get_customer(self, obj):
        return str(obj.cart.customer.person)

    @admin.display(description='Subtotal')
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"

