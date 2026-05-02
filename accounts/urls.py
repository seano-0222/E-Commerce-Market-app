"""
URL configuration for the accounts app.

Routes:
    /register/person/   → register_person   (create a Person)
    /register/customer/ → register_customer (assign Person as Customer)
    /register/vendor/   → register_vendor   (assign Person as Vendor)

These are included in the root URLconf via:
    path('', include('accounts.urls'))
"""

from django.urls import path

from . import views

urlpatterns = [
    # Index / home page
    path('',                   views.index,             name='index'),

    # Authentication
    path('login/',             views.login_view,        name='login'),
    path('logout/',            views.logout_view,       name='logout'),

    # Step 1 — create the base Person identity record
    path('register/person/',   views.register_person,   name='register_person'),

    # Step 2a — assign the Person as a Customer
    path('register/customer/', views.register_customer, name='register_customer'),

    # Step 2b — assign the Person as a Vendor
    path('register/vendor/',   views.register_vendor,   name='register_vendor'),
]
