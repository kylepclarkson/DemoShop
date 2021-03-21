from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def home(request):
    """ Display home page info. Included are featured products. """
    # products to be displayed in featured section
    featured = Product.objects.all().\
        filter(featured=True).\
        filter(available=True)

    context = {
        'featured': featured
    }
    return render(request, 'shop/home.html', context)


def product_list(request, category_slug=None):
    """ Get all products in a category. """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    """ Get a single product using its ID and slug. Fetch additional
    products with the same category as the requested product. """
    # include slug in URL to be SEO-friendly
    product = get_object_or_404(Product, id=id, slug=slug)
    category = product.category
    # 4 products in the same category, excluding the request.
    related_products = Product.objects.filter(category=category).exclude(id=id)[:4]

    # cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'related_products': related_products
        # 'cart_product_form': cart_product_form,
    }

    return render(request, 'shop/product/detail.html', context)


