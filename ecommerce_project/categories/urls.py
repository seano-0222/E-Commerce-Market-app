from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:category_id>/', views.category_detail, name='category_detail'),
    path('add/', views.add_category, name='add_category'),
    path('update/<int:category_id>/', views.update_category, name='update_category'),
    path('delete/<int:category_id>/', views.delete_category, name='delete_category'),
]