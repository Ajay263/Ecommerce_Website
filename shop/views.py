from django.shortcuts import get_object_or_404, render
from cart.forms import CartAddProductForm
from .models import Category, Product
from .recommender import Recommender


def product_list(request, category_slug=None):
    """Display a list of products, optionally filtered by category.

    This view retrieves all available products, and if a category slug
    is provided, it filters the products to only include those in the
    specified category.

    Args:
        request (HttpRequest): The HTTP request object.
        category_slug (str, optional): The slug of the category to filter products by.

    Returns:
        HttpResponse: The rendered product list template with context containing
        categories, filtered products, and the selected category.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    """Display the details of a specific product.

    This view retrieves the product based on its ID and slug. If the product
    is available, it displays its details along with a form to add the product
    to the cart and suggests related products based on purchase history.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the product to display.
        slug (str): The slug of the product to verify the correct product.

    Returns:
        HttpResponse: The rendered product detail template with context containing
        the product, cart product form, and recommended products.
    """
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products,
        },
    )
