from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('AddNewOrder/', views.add_new_order, name='add-new-order'),
    path('AddNewPlatform/', views.add_new_platform, name='add-new-platform'),
    path('EditProfile/', views.edit_profile, name='edit-profile'),
]