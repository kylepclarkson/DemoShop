from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

import braintree

from orders.models import Order
from .tasks import payment_completed
from cart.cart import Cart

# braintree gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_done(request):
    return render(request, 'payment/success.html')


def payment_cancel(request):
    return render(request, 'payment/error.html')


def payment_process(request):
    """
    Get order from session and attempt to get payment for it.
    If successful, send confirmation email to customer, clear contents of cart,
    and deactivate coupon if needed.
    """
    print("now here")
    cart = Cart(request)
    order_id = request.session.get('order_id')
    for item in cart:
        print(item)
    print(f'order id: {order_id}')
    order = get_object_or_404(Order, id=order_id)

    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction

        result = gateway.transaction.sale({
            "amount": f'{total_cost: 2f}',
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()

            # deactivate coupon
            coupon = cart.coupon
            if coupon.single_use:
                coupon.active = False
                coupon.save()

            # clear cart
            cart.clear()

            # send confirm email async.
            # payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            print(result.message)
            return redirect('payment:canceled')
    else:
        client_token = gateway.client_token.generate()
        context = {
            'order': order,
            'client_token': client_token
        }
        return render(request,
                      'payment/process.html',
                      context)

