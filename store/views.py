from django.shortcuts import render, get_object_or_404

# Create your views here.
from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)

    else:
        products = Product.objects.filter(is_available=True)

    context = {
        'products': products,
        'product_count': products.count()
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)