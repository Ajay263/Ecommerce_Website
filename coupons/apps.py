from django.apps import AppConfig


class CouponsConfig(AppConfig):
    """
    Configuration class for the 'coupons' app.

    This class defines application-specific settings for the 'coupons' app 
    and is responsible for configuring how the app behaves within the Django 
    project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupons'
   