from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
]
