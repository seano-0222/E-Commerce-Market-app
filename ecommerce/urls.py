"""
URL configuration for the E-Commerce Market project.
"""

from django.contrib import admin
from django.urls import path, include

from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.index, name='home'),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('reviews/', include('reviews.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('inventory/', include('inventory.urls')),
]
