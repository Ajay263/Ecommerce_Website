from decimal import Decimal

from coupons.models import Coupon
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Order(models.Model):
    """Represents an order placed by a customer.

    Attributes:
        first_name (CharField): Customer's first name.
        last_name (CharField): Customer's last name.
        email (EmailField): Customer's email address.
        address (CharField): Customer's shipping address.
        postal_code (CharField): Postal code for the shipping address.
        city (CharField): City for the shipping address.
        created (DateTimeField): The date and time the order was created.
        updated (DateTimeField): The date and time the order was last updated.
        paid (BooleanField): Indicates if the order has been paid.
        stripe_id (CharField): The Stripe payment ID associated with the order.
        coupon (ForeignKey): A coupon applied to the order (if any).
        discount (IntegerField): Discount percentage applied to the order.

    Methods:
        get_total_cost_before_discount(): Returns the total cost of the order before applying any discounts.
        get_discount(): Returns the discount amount based on the total cost and discount percentage.
        get_total_cost(): Returns the total cost after applying the discount.
        get_stripe_url(): Returns the URL to view the payment on the Stripe dashboard.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        """Returns a string representation of the order."""
        return f'Order {self.id}'

    def get_total_cost_before_discount(self):
        """Calculates the total cost of the order before any discount.

        Returns:
            Decimal: The total cost before discount.
        """
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        """Calculates the discount amount based on the discount percentage.

        Returns:
            Decimal: The discount amount to be subtracted from the total cost.
        """
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        """Calculates the total cost of the order after applying the discount.

        Returns:
            Decimal: The total cost after discount.
        """
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        """Generates the URL for viewing the payment in the Stripe dashboard.

        Returns:
            str: The Stripe URL for viewing the payment or an empty string if no Stripe ID exists.
        """
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    """Represents an item in an order.

    Attributes:
        order (ForeignKey): The order to which this item belongs.
        product (ForeignKey): The product that was ordered.
        price (DecimalField): The price of the product.
        quantity (PositiveIntegerField): The quantity of the product ordered.

    Methods:
        get_cost(): Calculates the total cost for the ordered quantity of the product.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """Returns a string representation of the order item."""
        return str(self.id)

    def get_cost(self):
        """Calculates the total cost for the ordered quantity of the product.

        Returns:
            Decimal: The total cost for this order item.
        """
        return self.price * self.quantity
