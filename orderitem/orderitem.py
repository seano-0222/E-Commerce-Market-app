from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='orderitem-index'),
    path('AddNewOrderItem/', views.add_new_order_item, name='add-new-orderitem'),
]