from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ A category of a shop product. """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):

    categories = models.ManyToManyField(Category, related_name='products')
    # we query both name and slug; use db_index.
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              default='products/no_image.png')
    description = models.TextField(blank=True)
    # use DecimalField instead of float to avoid rounding issues.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # quantity = models.PositiveIntegerField(default=0)
    # false if product cannot be bought.
    available = models.BooleanField(default=True)
    # These items will require a mailing address.
    is_physical = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_categories(self):
        return [category for category in self.categories.iterator()]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

