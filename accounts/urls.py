""" URL configuration for the accounts app. """

from django.urls import path
from . import views


urlpatterns = [
    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ------------------------------------------------------------------
    # Home (after login)
    # ------------------------------------------------------------------
    path('', views.index, name='index'),  # HOME PAGE

    # ------------------------------------------------------------------
    # NEW FEATURES (Required in Project V2)
    # ------------------------------------------------------------------
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-record/', views.add_record, name='add_record'),

    # ------------------------------------------------------------------
    # Existing Features (DO NOT REMOVE)
    # ------------------------------------------------------------------
    path('register/person/', views.register_person, name='register_person'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/vendor/', views.register_vendor, name='register_vendor'),
]