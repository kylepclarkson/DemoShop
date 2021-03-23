from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # discount percentage.
    discount = models.IntegerField(validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])
    # coupon has been used.
    active = models.BooleanField()
    # true if coupon can only be used once.
    single_use = models.BooleanField(default=True)

    def __str__(self):
        return self.code

