from carts.models import CartItem, Cart
from carts.views import _cart_id


def counter(request):
    if 'admin' in request.path:
         return {}
    else:
        cart_count = 0
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1])

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
           pass

    return dict(cart_count=cart_count)
