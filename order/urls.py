from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='order-index'),
    path('AddNewOrder/', views.add_new_order, name='add-new-order'),
    path('AddNewPlatform/', views.add_new_platform, name='add-new-platform'),
]