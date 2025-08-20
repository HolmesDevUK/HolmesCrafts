from .services import set_nav, set_nav_cards
from cart.services import in_basket

def set_nav_bar(request):

    return {
        "nav_bar": set_nav(),
        "nav_bar_cards": set_nav_cards()
    }


def in_basket(request):

    return {
        "in_cart": in_basket(request)
    }