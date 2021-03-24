import csv
import datetime

from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import OrderItem, Order


def order_detail(obj):
    """ Admin item. Link to view order detail. """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'paid', 'created', 'updated',]
                    # order_detail, order_pdf]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    # actions = [export_to_csv]