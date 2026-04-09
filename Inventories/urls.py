from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('<int:inventory_id>/', views.inventory_detail, name='inventory_detail'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/<int:warehouse_id>/', views.warehouse_detail, name='warehouse_detail'),
]
