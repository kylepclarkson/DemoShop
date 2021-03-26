from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.core import serializers
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    """
    Create a new order using cart contents and apply discount if present.
    Then redirect user to payment form to complete order.
    """
    cart = Cart(request)

    # empty cart, redirect user products page.
    if len(cart) == 0:
        return redirect('shop:product_list')

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            # apply coupon, discount if present
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            # create OrderItem instances for each item in cart.
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # todo move remaining code to occur only after payment is successful.
            # clear cart
            # cart.clear()
            # send email asynchronously
            # order_created.delay(order.id)
            # set order in session
            del request.session['order_id']
            request.session['order_id'] = str(order.id)
            # request.session['order_id'] = serializers.serialize('json', Order.objects.get(id=order.id))
            # redirect for payment
            # todo: by not clearing cart, its contents (Decimal values) need to be json serializable to use
            # todo this redirect. Read up on Django Sessions.
            print("here")
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_pdf(request, order_id):
    """ Generate a pdf of the order with given id. """
    """ Issue using weasyprint. Commented out. """
    pass
    # order = get_object_or_404(Order, id=order_id)
    # # render order
    # html = render_to_string('orders/order/pdf.html', {'order': order})
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'filename=order_{order_id}.pdf'
    # weasyprint.HTML(string=html).write_pdf(
    #     response,
    #     stylesheets=[weasyprint.CSS(
    #         settings.STATIC_ROOT + 'css/pdf.css'
    #     )]
    # )
    # return response


@staff_member_required
def admin_order_detail(request, order_id):
    """ An admin view to see order details. """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})