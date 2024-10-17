from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Model representing a product category.

    Attributes:
        name (CharField): The name of the category.
        slug (SlugField): A unique slug for the category.

    Meta:
        ordering (list): Default ordering of categories by name.
        indexes (list): Database indexes for efficient querying.
        verbose_name (str): Singular name for the category.
        verbose_name_plural (str): Plural name for categories.
    """
    name = models.CharField(max_length=200)  # The name of the category
    slug = models.SlugField(max_length=200, unique=True)  # Unique slug for URL

    class Meta:
        ordering = ['name']  # Default ordering of categories by name
        indexes = [
            models.Index(fields=['name']),  # Index for the name field
        ]
        verbose_name = 'category'  # Singular name for the category
        verbose_name_plural = 'categories'  # Plural name for categories

    def __str__(self):
        """Return the string representation of the category."""
        return self.name

    def get_absolute_url(self):
        """Return the URL to access a list of products in this category.

        Returns:
            str: URL for the product list of this category.
        """
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """Model representing a product.

    Attributes:
        category (ForeignKey): The category this product belongs to.
        name (CharField): The name of the product.
        slug (SlugField): A slug for the product.
        image (ImageField): The image of the product.
        description (TextField): Description of the product.
        price (DecimalField): Price of the product.
        available (BooleanField): Availability status of the product.
        created (DateTimeField): The date the product was created.
        updated (DateTimeField): The date the product was last updated.

    Meta:
        ordering (list): Default ordering of products by name.
        indexes (list): Database indexes for efficient querying.
    """
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )  # The category this product belongs to
    name = models.CharField(max_length=200)  # The name of the product
    slug = models.SlugField(max_length=200)  # Slug for the product
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )  # The image of the product
    description = models.TextField(blank=True)  # Description of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product
    available = models.BooleanField(default=True)  # Availability status
    created = models.DateTimeField(auto_now_add=True)  # Date created
    updated = models.DateTimeField(auto_now=True)  # Date last updated

    class Meta:
        ordering = ['name']  # Default ordering of products by name
        indexes = [
            models.Index(fields=['id', 'slug']),  # Index for ID and slug fields
            models.Index(fields=['name']),  # Index for the name field
            models.Index(fields=['-created']),  # Index for created date (descending)
        ]

    def __str__(self):
        """Return the string representation of the product."""
        return self.name

    def get_absolute_url(self):
        """Return the URL to access the detail view of this product.

        Returns:
            str: URL for the product detail page.
        """
        return reverse('shop:product_detail', args=[self.id, self.slug])
