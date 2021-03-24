from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    """ User attempts to apply coupon code. """
    now = timezone.now()
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
            messages.add_message(request,
                                 messages.ERROR,
                                 f'Coupon "{code}" applied to cart.',
                                 extra_tags='bg-primary text-white')
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            # Coupon does not exist or is invalid.
            messages.add_message(request,
                                 messages.ERROR,
                                 f'Coupon "{code}" is either invalid or does not exist!',
                                 extra_tags='bg-danger text-white')

        return redirect('cart:cart_detail')

    else:
        print(form.errors)


def coupon_remove(request):
    """ Removes applied coupon's effects. """
    request.session['coupon_id'] = None

    return redirect('cart:cart_detail')
