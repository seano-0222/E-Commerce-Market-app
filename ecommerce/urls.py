from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('order.urls')),
    path('Order/', include('order.urls')),
    path('OrderItem/', include('orderitem.urls')),
    path('Payment/', include('payment.urls')),
    path('Shipment/', include('shipment.urls')),
]