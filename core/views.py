from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import Card, Notebook

class HomeView(ListView):
    template_name = "holmescraftsuk/index.html"
    model = Card
    context_object_name = "cards"

    def get_context_data(self, **kwargs):
        notebooks = Notebook.objects.filter(is_featured=True)
        birthday_cards = Card.objects.filter(card_type="Birthday").filter(is_featured=True)
        wedding_cards = Card.objects.filter(card_type="Wedding").filter(is_featured=True)
        seasonal_cards = Card.objects.filter(card_type="Seasonal").filter(is_featured=True)
        special_cards = Card.objects.filter(card_type="Special Occasion").filter(is_featured=True)
        other_cards = Card.objects.filter(card_type="Other").filter(is_featured=True)
        context = super().get_context_data(**kwargs)
        context["notebooks"] = notebooks
        context["birthday_cards"] = birthday_cards
        context["wedding_cards"] = wedding_cards
        context["seasonal_cards"] = seasonal_cards
        context["special_cards"] = special_cards
        context["other_cards"] = other_cards
        context["nav_bar"] = set_nav()
        context["nav_bar_cards"] = set_nav_cards()
        context["current_page"] = "HOME"
        context["in_cart"] = in_basket(self.request)
        return context
