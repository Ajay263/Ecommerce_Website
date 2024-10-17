from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for managing product categories.

    Attributes:
        list_display (list): Fields to display in the admin list view.
        prepopulated_fields (dict): Fields that are automatically populated based on other fields.
    """
    list_display = ['name', 'slug']  # Fields to display in the list view
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug based on name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for managing products.

    Attributes:
        list_display (list): Fields to display in the admin list view.
        list_filter (list): Fields to filter the list view.
        list_editable (list): Fields that can be edited directly in the list view.
        prepopulated_fields (dict): Fields that are automatically populated based on other fields.
    """
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated',
    ]  # Fields to display in the list view

    list_filter = ['available', 'created', 'updated']  # Filter options for the list view
    list_editable = ['price', 'available']  # Editable fields in the list view
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug based on name
