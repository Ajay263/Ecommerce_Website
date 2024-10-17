from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    Form to handle adding a product to the cart.

    Fields:
        quantity (TypedChoiceField): The quantity of the product to add, with choices ranging from 1 to 20.
        override (BooleanField): A hidden field to determine if the quantity should be overridden or updated.
    """
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
