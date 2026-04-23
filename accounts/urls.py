from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-person/', views.add_person, name='add_person'),
    path('addNewPerson/', views.add_person, name='add_new_person'),
    path('add-vendor/', views.add_vendor, name='add_vendor'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/person/', views.register_person, name='register_person'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
]
