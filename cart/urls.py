"""
URL configuration for the cart app (Malubay).

Routes:
    /cart/                      → view_cart
    /cart/add/<product_id>/     → add_to_cart
    /cart/remove/<item_id>/     → remove_from_cart
    /cart/clear/                → clear_cart
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.view_cart,        name='view_cart'),
    path('add/<int:product_id>/',   views.add_to_cart,      name='add_to_cart'),
    path('remove/<int:item_id>/',   views.remove_from_cart, name='remove_from_cart'),
    path('clear/',                  views.clear_cart,       name='clear_cart'),
    path('addNewCart',              views.add_new_cart, name='add_new_cart'),
]
