from .cart import Cart

def cart(request):
    """
    Context processor to add the cart to the context of every template.

    Args:
        request (HttpRequest): The HTTP request object containing session data.

    Returns:
        dict: A dictionary containing the cart object.
    """
    return {'cart': Cart(request)}
