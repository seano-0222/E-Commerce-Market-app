from django.contrib import admin
from django.urls import path, include
from . import views
from accounts.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # Use custom logout view
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('reviews/', include('reviews.urls')),
]