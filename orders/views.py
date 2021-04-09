import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

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
    Called once payment is successful. Creates a new order instances, empties cart, and sends email confirmation email.
    """
    cart = Cart(request)

    # empty cart, redirect user products page.
    if len(cart) == 0:
        return redirect('shop:product_list')

    if request.method == "POST":
        data = json.loads(request.body)
        print("data:", data)
        form_contact_data = data['form_contact_data']
        order_id = data['order_id']

        order = Order.objects.create(
            first_name=form_contact_data['first_name'],
            last_name=form_contact_data['last_name'],
            email=form_contact_data['email'],
            paid=True,
            order_id=order_id,
        )
        if cart.contains_physical():
            # attach mailing address to order
            order.address = form_contact_data['address']
            order.postal_code = form_contact_data['postal_code']

        if cart.coupon:
            # attach coupon
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
        # clear cart
        cart.clear()
        # send email asynchronously
        # order_created.delay(order.id)

        # display message
        messages.add_message(request,
                             messages.SUCCESS,
                             f'Order placed! Check your email for a confirmation shortly.',
                             extra_tags='bg-success text-white')
        print("order created")
        return JsonResponse('Payment complete', safe=False)

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


def order_test(request):
    """ Testing receiving data from javascript request. """

    form_contact_data = json.loads(request.body)

    print(f'form data: ', form_contact_data)

    return HttpResponse('hello')

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
