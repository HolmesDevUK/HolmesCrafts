from .services import set_nav, set_nav_cards
from cart.services import get_cart_count

def set_nav_bar(request):

    return {
        "nav_bar": set_nav(),
        "nav_bar_cards": set_nav_cards()
    }


def cart_count(request):

    return {
        "in_cart": get_cart_count(request)
    }