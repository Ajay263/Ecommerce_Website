from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Coupon objects.

    This class defines the customization of how the Coupon model will 
    be displayed and managed within the Django admin interface.
    """

    list_display = [
        'code',
        'valid_from',
        'valid_to',
        'discount',
        'active',
    ]
    """
    list_display: Specifies the fields to display on the Coupon list view in 
    the admin interface. The fields shown are the coupon code, validity range, 
    discount percentage, and whether the coupon is currently active.
    """

    list_filter = ['active', 'valid_from', 'valid_to']
    """
    list_filter: Adds filtering options in the right sidebar of the Coupon list 
    view. Admins can filter coupons based on their 'active' status and validity 
    dates ('valid_from' and 'valid_to').
    """

    search_fields = ['code']
    """
    search_fields: Enables a search box in the Coupon list view, allowing admins 
    to search for coupons by their 'code' field.
    """
