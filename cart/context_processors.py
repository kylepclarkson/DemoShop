from .cart import Cart
"""
A cart context processor that makes the cart available to all templates.
Registered in settings.py 
"""


def cart(request):
    return {
        'cart': Cart(request),
    }
