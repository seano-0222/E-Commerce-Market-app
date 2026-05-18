from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('',                    views.inventory_list,   name='inventory_list'),
    path('add-new-record',      views.add_new_record,   name='add_new_record'),
    path('warehouses/',         views.warehouse_list,   name='warehouse_list'),
=======
    path('', views.inventory_list, name='inventory_list'),
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
>>>>>>> 827cfe0f4065836dd040e1de6a34ee991ea04f14
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
]
