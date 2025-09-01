from .models import Cart

def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True)
        if guest_cart and guest_cart != cart:
            merge_carts(cart, guest_cart)
        cart.session_key = session_key
        cart.save()
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)

    return cart


def merge_carts(user_cart, guest_cart):
    for item in guest_cart.items.all():
        user_item, created = user_cart.items.get_or_create(product=item.product)
        if not created:
            user_item.quantity += item.quantity
            user_item.save()
    guest_cart.delete()


        