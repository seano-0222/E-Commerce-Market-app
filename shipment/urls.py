from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shipment-index'),
    path('AddNewShipment/', views.add_new_shipment, name='add-new-shipment'),
]