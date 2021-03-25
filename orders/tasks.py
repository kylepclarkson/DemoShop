from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """ An order has successfully been created by a customer.
        Send an email to the customer informing them as such.
    """

    # todo send email to admin as well.

    order = Order.objects.get(id=order_id)
    subject = f'Order {order.id} Placed!'
    message = f'Dear {order.first_name}, \n\n' \
              f'Your order with ID {order.id} has been placed!\n\n' \
              f'Thank you for shopping with us. Have a great day!'
    mail_sent = send_mail(subject, message, 'admin@myshop.ca', [order.email])

    return mail_sent