# from celery import shared_task
from django.core.mail import send_mail
from DemoShop import private_keys as prikeys

from .models import Order


# @shared_task
def order_created(order_id):
    """ An order has successfully been created by a customer.
        Send an email to the customer informing them as such.
    """

    # todo send email to admin as well.

    order = Order.objects.get(id=order_id)
    subject = f'Order placed - The DemoShop'
    message = f'Dear {order.first_name}, \n\n' \
              f'Your order with ID {order.order_id} has been placed!\n\n' \
              f'Thank you for shopping with us. Have a great day!\n\n' \
              f'- The DemoShop'
    mail_sent = send_mail(subject, message, prikeys.EMAIL_HOST_USER, [order.email, prikeys.EMAIL_HOST_USER])

    return mail_sent