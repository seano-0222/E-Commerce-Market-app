"""
URL configuration for the E-Commerce Market project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect bare root URL to the person registration page
    path('', RedirectView.as_view(pattern_name='register_person', permanent=False)),
    # Include all accounts app URLs
    path('', include('accounts.urls')),
]
