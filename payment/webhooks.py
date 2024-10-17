import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from shop.models import Product
from shop.recommender import Recommender
from .tasks import payment_completed

@csrf_exempt
def stripe_webhook(request):
    """
    Handles Stripe webhook events for payment processing.

    This view listens for webhook events sent by Stripe. It verifies the 
    signature of the event and processes it accordingly. Specifically, 
    it handles the `checkout.session.completed` event to update the 
    order status, store the payment ID, and trigger product recommendations.

    Args:
        request (HttpRequest): The request object containing metadata about the request.

    Returns:
        HttpResponse: A response indicating the success or failure of the webhook 
                      event processing. Returns 200 for success and appropriate 
                      error codes for failure cases.
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        # Verify the Stripe webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event type
    if event.type == 'checkout.session.completed':
        session = event.data.object
        
        # Check if the session is for a successful payment
        if (
            session.mode == 'payment'
            and session.payment_status == 'paid'
        ):
            try:
                # Retrieve the order associated with the session
                order = Order.objects.get(
                    id=session.client_reference_id
                )
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            # Mark order as paid
            order.paid = True

            # Store the Stripe payment ID in the order
            order.stripe_id = session.payment_intent
            order.save()

            # Save items bought for product recommendations
            product_ids = order.items.values_list('product_id', flat=True)
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.products_bought(products)

            # Launch asynchronous task to process payment completion
            payment_completed.delay(order.id)

    return HttpResponse(status=200)
