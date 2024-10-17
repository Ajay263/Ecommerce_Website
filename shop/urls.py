from django.urls import path

from . import views

app_name = 'shop'

"""
URL configuration for the shop app.

This module defines URL patterns for accessing product-related views,
including a list of products, filtering products by category, and
displaying details of a specific product.

Available URL patterns:
- `product_list`: Displays all products.
- `product_list_by_category`: Displays products filtered by the specified category.
- `product_detail`: Displays the details of a specific product.
"""

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category',
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail',
    ),
]
