from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    """Apply a coupon code to the shopping cart.

    This view function handles the POST request for applying a coupon code. 
    It validates the provided code and checks if the coupon is active and within its valid date range. 
    If valid, the coupon ID is stored in the session; otherwise, it sets the coupon ID to None.

    Args:
        request: The HTTP request object containing the form data.

    Returns:
        HttpResponse: Redirects the user to the cart detail page after processing the coupon.
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
