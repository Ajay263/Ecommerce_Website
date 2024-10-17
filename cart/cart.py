from decimal import Decimal

from coupons.models import Coupon
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.

        Args:
            request (HttpRequest): The HTTP request object containing session data.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.

        Yields:
            dict: A dictionary containing product details, price, quantity, and total price.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.

        Returns:
            int: Total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.

        Args:
            product (Product): The product to be added or updated in the cart.
            quantity (int, optional): Number of units of the product to add. Defaults to 1.
            override_quantity (bool, optional): Whether to override the existing quantity. Defaults to False.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as "modified" to ensure it is saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.

        Args:
            product (Product): The product to remove from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Remove the cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.

        Returns:
            Decimal: The total price of the cart.
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    @property
    def coupon(self):
        """
        Get the currently applied coupon.

        Returns:
            Coupon or None: The applied coupon object, or None if no coupon is applied.
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        Calculate the discount based on the applied coupon.

        Returns:
            Decimal: The discount amount. If no coupon is applied, returns 0.
        """
        if self.coupon:
            return (
                self.coupon.discount / Decimal(100)
            ) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """
        Calculate the total price after applying the coupon discount.

        Returns:
            Decimal: The total price after the discount is applied.
        """
        return self.get_total_price() - self.get_discount()
