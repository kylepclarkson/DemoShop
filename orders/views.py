from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

# xhtml2pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

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

        if not cart.contains_physical():
            # disable requirements if not needed.
            form.fields['address'].required = False
            form.fields['postal_code'].required = False

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
            # TODO do not clear cart, jsonify OrderItems
            # clear cart
            cart.clear()
            # send email asynchronously
            # order_created.delay(order.id)
            # set order in session
            # redirect for payment
            request.session['order_id'] = order.id
            print("here")
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()
        if not cart.contains_physical():
            # hide mailing inputs in form
            from django import forms
            form.fields['address'].widget = forms.HiddenInput()
            form.fields['postal_code'].widget = forms.HiddenInput()

    context = {
        'cart': cart,
        'create_order_form': form,
    }
    return render(request, 'orders/order/create.html', context=context)


@staff_member_required
def admin_order_pdf(request, order_id):
    """ Generate a pdf of the order with given id. """
    # pass
    order = get_object_or_404(Order, id=order_id)
    # render order
    template_path = 'orders/order/pdf.html'
    context = {'order': order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@staff_member_required
def admin_order_detail(request, order_id):
    """ An admin view to see order details. """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
