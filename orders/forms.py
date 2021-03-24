from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
        A form presented to the user when they create a new order.
        Presented after user moves from cart to checkout, and before
        entering payment details.
     """

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code',]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mailing Address',
                'required': True
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal Code (e.g. A1A 1A1)',
                'required': True
            }),
        }
