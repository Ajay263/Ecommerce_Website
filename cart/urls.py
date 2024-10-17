from django.urls import path
from . import views

app_name = 'cart'

"""
URL configuration for the cart application.

Includes routes for viewing the cart, adding a product to the cart, and removing a product from the cart.

Routes:
    - '' (cart_detail): View the details of the current cart.
    - 'add/<int:product_id>/' (cart_add): Add a product to the cart by product ID.
    - 'remove/<int:product_id>/' (cart_remove): Remove a product from the cart by product ID.
"""

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
