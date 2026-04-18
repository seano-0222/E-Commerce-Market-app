from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='payment-index'),
    path('AddNewPayment/', views.add_new_payment, name='add-new-payment'),
]