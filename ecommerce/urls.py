"""
URL configuration for the E-Commerce Market project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # All accounts app URLs (includes index at /)
    path('', include('accounts.urls')),
]
