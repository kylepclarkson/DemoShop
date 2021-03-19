from django import forms

# Users can choose a quantity in [1,20] items to add to the cart.
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # whether or not we override the previous quantity of this item in the cart.
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)