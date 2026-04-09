from django.contrib import admin
from .models import Platform, Order, OrderItem, Payment, Shipment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0


class ShipmentInline(admin.TabularInline):
    model = Shipment
    extra = 0


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'platform', 'order_date', 'status', 'total_amount')
    list_filter = ('status', 'platform')
    search_fields = ('customer__person__email',)
    inlines = [OrderItemInline, PaymentInline, ShipmentInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'payment_date', 'amount', 'payment_method')
    list_filter = ('payment_method',)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'shipment_date', 'status', 'delivery_address', 'quantity')
    list_filter = ('status',)
