from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Form for creating a new order.

    This form is used to collect customer information for creating an order.

    Attributes:
        Meta: Defines the model and fields to include in the form.
    """
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'postal_code',
            'city',
        ]
