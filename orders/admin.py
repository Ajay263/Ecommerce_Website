import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    """Export selected orders to a CSV file.

    Args:
        modeladmin (ModelAdmin): The model admin class.
        request (HttpRequest): The HTTP request object.
        queryset (QuerySet): The queryset of selected objects.

    Returns:
        HttpResponse: The response object containing the CSV data.
    """
    opts = modeladmin.model._meta
    content_disposition = (
        f'attachment; filename={opts.verbose_name}.csv'
    )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    
    # Get all fields excluding many-to-many and one-to-many fields
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    
    # Write the header row
    writer.writerow([field.verbose_name for field in fields])
    
    # Write data rows for each selected object
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            # Format datetime fields to a readable format
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    
    return response

export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    """Inline admin class for order items in the order admin interface."""
    model = OrderItem
    raw_id_fields = ['product']


def order_payment(obj):
    """Generate a link to the Stripe payment page for the order.

    Args:
        obj (Order): The order object.

    Returns:
        str: A safe HTML link to the Stripe payment page or an empty string.
    """
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Stripe payment'


def order_detail(obj):
    """Generate a link to the admin order detail view.

    Args:
        obj (Order): The order object.

    Returns:
        str: A safe HTML link to the order detail view.
    """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    """Generate a link to download the order invoice as a PDF.

    Args:
        obj (Order): The order object.

    Returns:
        str: A safe HTML link to download the PDF invoice.
    """
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for managing orders."""
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        order_payment,
        'created',
        'updated',
        order_detail,
        order_pdf,
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
