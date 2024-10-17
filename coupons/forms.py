from django import forms


class CouponApplyForm(forms.Form):
    """
    Form for applying a coupon code during checkout.

    This form consists of a single field where the user can input a coupon code
    to apply a discount during the purchase process.
    """
    code = forms.CharField()
    