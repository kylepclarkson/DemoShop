from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from io import BytesIO
from celery import shared_task

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """ Send email when order is successfully created."""
    order = Order.objects.get(id=order_id)

    subject = f'DemoShop - Order no. {order.id} confirmed'
    message = f'Dear {order.first_name}, \n\n' \
              f'This email confirms your order with ID {order.id} has been ' \
              f'received and paid for (in the demo sense.) Expect a follow-up email in a few days ' \
              f'to notify you when your order is sent to the address provided (is how this email would continue if you '\
              f'actually purchased anything, which you haven\'t.) \n\n' \
              f'Despite this thank you for your business/interest!\n'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    email.send()
