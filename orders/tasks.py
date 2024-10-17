from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.

    Args:
        order_id (int): The ID of the created order.

    Returns:
        int: The number of successfully delivered emails (1 if sent successfully, 0 otherwise).

    This task retrieves the order by its ID, constructs an email message containing the 
    order details, and sends it to the customer. The email confirms that the order has 
    been successfully placed.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'You have successfully placed an order.'
        f'Your order ID is {order.id}.'
    )
    mail_sent = send_mail(
        subject, message, 'admin@myshop.com', [order.email]
    )
    return mail_sent
