from .services import set_nav, set_nav_cards
from cart.utils import get_cart

def set_nav_bar(request):

    return {
        "nav_bar": set_nav(),
        "nav_bar_cards": set_nav_cards()
    }


def cart_count(request):

    cart = get_cart(request)
    return {
        "in_cart": cart.total_quantity() if cart else 0
    }