from .models import Navbar

def set_nav():
    nav_bar = Navbar.objects.filter(is_card=False)

    return nav_bar

def set_nav_cards():
    nav_bar_cards = Navbar.objects.filter(is_card=True)

    return nav_bar_cards