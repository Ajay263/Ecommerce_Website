from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product
from shop.recommender import Recommender
from coupons.forms import CouponApplyForm

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart or update its quantity.

    This view handles POST requests to add a product to the cart.
    If the product is already in the cart, the quantity is updated
    based on the form data.

    Args:
        request (HttpRequest): The HTTP request object containing POST data.
        product_id (int): The ID of the product to add to the cart.

    Returns:
        HttpResponseRedirect: Redirects to the cart detail page after adding the product.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
        )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.

    This view handles POST requests to remove a product from the cart.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to remove from the cart.

    Returns:
        HttpResponseRedirect: Redirects to the cart detail page after removing the product.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Display the details of the cart.

    This view shows the products in the cart, allows quantity updates,
    and suggests recommended products based on the items in the cart.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the cart detail page with the cart contents, coupon form, 
                      and recommended products.
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(
            cart_products, max_results=4
        )
    else:
        recommended_products = []

    return render(
        request,
        'cart/detail.html',
        {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products,
        },
    )
