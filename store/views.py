from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')

    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    paginator = Paginator(products,3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': products.count()
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    context = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count':  product_count,
    }
    return render(request, 'store/store.html', context)