"""
URL configuration for the E-Commerce Market project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts app (Tormes) — includes index, login, register
    path('', include('accounts.urls')),
    # Categories app (Alipin)
    path('categories/', include('categories.urls')),
    # Products app (Alipin)
    path('products/', include('products.urls')),
    # Reviews app (Alipin)
    path('reviews/', include('reviews.urls')),
    # Cart app (Malubay)
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]
