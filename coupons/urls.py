from django.urls import path

from . import views

app_name = 'coupons'

"""
URL pattern for applying a coupon.

This URL pattern routes requests to the `coupon_apply` view, which handles
the logic for applying a coupon to a cart.

Args:
    path: The URL path for the coupon application.
    views.coupon_apply: The view function that will be called when this URL is accessed.
    name: The name of the URL pattern, which can be used for reverse lookups.
"""

urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),

]
