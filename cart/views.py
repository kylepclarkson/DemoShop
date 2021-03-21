from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


def cart_detail(request):
    """ Get current cart. """
    cart = Cart(request)
    # provide form to edit order quantity.
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            }
        )
    coupon_apply_form = CouponApplyForm()

    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    }

    return render(request, 'cart/detail.html', context)


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.quantity > 0:
        # place item in cart.
        product.quantity -= 1
        product.save()
        cart.add(product=product, quantity=1, override_quantity=True)

        toast_message = f"{product.name} added to cart."
        toast_bg = "bg-success"

    else:
        # item is no longer available
        toast_message = f"{product.name} is no longer available!"
        toast_bg = "bg-danger"

    context = {
        toast_message: toast_message,
        toast_bg: toast_bg
    }

    
# @require_POST
# def cart_add(request, product_id):
#     """ Add product to cart. """
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
#     return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """ Remove product from cart. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

