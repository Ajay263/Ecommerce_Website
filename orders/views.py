import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    """
    Handle order creation and processing.

    This view handles the process of creating an order based on the user's
    cart and order form submission. If the form is valid, an order is created,
    order items are saved, the cart is cleared, and an asynchronous task is
    launched to send a confirmation email. The order is saved in the session,
    and the user is redirected to the payment process.

    Args:
        request (HttpRequest): The HTTP request object containing user data
            and the POST data from the order form.

    Returns:
        HttpResponse: If the form is submitted and valid, redirects to the 
        payment process page. Otherwise, renders the order creation form
        template.
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )


@staff_member_required
def admin_order_detail(request, order_id):
    """
    Display the details of a specific order in the admin panel.

    This view is restricted to staff members and displays the details of
    a given order, such as customer information, items bought, and order
    total, using a template.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (int): The ID of the order to be retrieved and displayed.

    Returns:
        HttpResponse: Renders the admin order detail template.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, 'admin/orders/order/detail.html', {'order': order}
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    Generate a PDF invoice for a specific order in the admin panel.

    This view generates a PDF version of the invoice for the specified order,
    restricted to staff members. It uses the WeasyPrint library to render
    HTML to PDF.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (int): The ID of the order for which the PDF invoice is generated.

    Returns:
        HttpResponse: A response object containing the generated PDF, with
        appropriate content type and headers for downloading the file.
    """
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))],
    )
    return response
