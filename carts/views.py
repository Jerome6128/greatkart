from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from carts.models import Cart, CartItem
from store.models import Product, Variation


def cart(request, total=0, quantity=0, cart_items=0):
    tax = 0
    grand_total = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity = cart_item.quantity
        tax = 20 / 100 * total
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'tax' : tax,
        'grand_total' : grand_total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    product_variation.append(Variation.objects.get(product=product, variation_category__iexact=key,
                                                                   variation_value__iexact=value))
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item = CartItem.objects.get(product=product, id=id[index])
                item.quantity += 1
                item.save()
                return redirect('cart')

        item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=current_user,
        )

        item.variations.add(*product_variation)

        item.save()
        return redirect('cart')

    else:
        product_variation= []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    product_variation.append(Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value))
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )

        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                ex_var_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item = CartItem.objects.get(product=product, id=id[index])
                item.quantity += 1
                item.save()
                return redirect('cart')

        item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )

        item.variations.add(*product_variation)

        item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    item = CartItem.objects.get(id=cart_item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    item = CartItem.objects.get(id=cart_item_id)

    item.delete()

    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    current_user = request.user
    try:
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity = cart_item.quantity
        tax = 20 / 100 * total
        grand_total = total + tax
    except Cart.DoesNotExist:
        print('except block')

    context = {
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)