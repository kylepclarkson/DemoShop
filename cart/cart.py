from decimal import Decimal
from django.conf import settings

from shop.models import Product
from coupons.models import Coupon


class Cart(object):

    """
    A cart object where users can store items while browsing the site. The cart field is a dictionary
    where keys are product ids and values are dictionaries. The value dictionaries have string keys
    'quantity' and 'price' which store integers and price of item (when added to cart) respectively.

    """

    def __init__(self, request):
        """ Get (or create) cart session of user. """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # No cart instance existed in session. Create one.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store coupon from session object.
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """ Add/update a product to the cart. """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.session_updated()

    def remove(self, product):
        """ Remove a product from the cart """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session_updated()

    def clear(self):
        """ Remove cart from session. """
        del self.session[settings.CART_SESSION_ID]
        self.session_updated()

    def get_total_price(self):
        """ Return total price of shopping cart. """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        """ Get coupon for this cart session. """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """ Returns discount price of cart. """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """ Returns price after applying coupon discount. """
        return self.get_total_price() - self.get_discount()

    def __len__(self):
        """ Return the number of items in the cart """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """ Return an iteration of all items in the cart. """
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # convert to decimal object.
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def session_updated(self):
        """ Mark session as updated so it gets saved. """
        self.session.modified = True