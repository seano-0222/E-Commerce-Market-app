from django.contrib import admin
from .models import Platform, Order, OrderItem, Payment, Shipment

admin.site.register(Platform)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Shipment)