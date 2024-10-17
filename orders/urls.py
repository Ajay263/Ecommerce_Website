from django.urls import path

from . import views


app_name = 'orders'
"""
URL patterns for the 'orders' application.

This module defines the URL patterns for managing customer orders, including 
creating orders and viewing admin-related details for an order.

Paths:
    - 'create/': Displays the order creation form and handles order submission.
    - 'admin/order/<int:order_id>/': Displays detailed order information for the 
      specified `order_id` in the admin view.
    - 'admin/order/<int:order_id>/pdf/': Generates a PDF invoice for the specified 
      `order_id`.

Attributes:
    app_name (str): The name of the application, used for namespacing the URLs.
"""
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path(
        'admin/order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail',
    ),
    path(
        'admin/order/<int:order_id>/pdf/',
        views.admin_order_pdf,
        name='admin_order_pdf',
    ),
]
