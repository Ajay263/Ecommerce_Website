from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    """
    Represents a discount coupon that can be applied to a purchase.

    Attributes:
        code (str): The unique code for the coupon.
        valid_from (datetime): The date and time when the coupon becomes valid.
        valid_to (datetime): The date and time when the coupon expires.
        discount (int): The discount percentage applied by the coupon (0-100).
        active (bool): Indicates whether the coupon is currently active.
    """

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentage value (0 to 100)',
    )
    active = models.BooleanField()
   
   

    def __str__(self):
        """
        String representation of the Coupon object, returning its code.
        
        Returns:
            str: The coupon code.
        """
        return self.code
