from django.shortcuts import render
from django.views.generic.base import TemplateView

from catalog.models import Card, Notebook

class HomeView(TemplateView):
    template_name = "holmescraftsuk/index.html"

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
        context["current_page"] = "HOME"
        return context
