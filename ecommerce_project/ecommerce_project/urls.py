from django.contrib import admin
from django.urls import path, include
from . import views
from accounts.views import login_view, logout_view, register_view, edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('reviews/', include('reviews.urls')),
]
