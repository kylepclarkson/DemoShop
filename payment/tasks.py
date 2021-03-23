from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from io import BytesIO
from celery import task
# import weasyprint

from orders.models import Order


@task
def payment_completed(order_id):
    """ Send email when order is successfully created."""
    print(f'Order id {order_id}')
    order = Order.objects.get(id=order_id)

    subject = f'My shop - Order no. {order.id} confirmed'
    message = 'This email confirms your order. Thank you.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    email.send()
