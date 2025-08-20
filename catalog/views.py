from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Card, Notebook

class NotebooksView(ListView):
    template_name = "holmescraftsuk/notebooks.html"
    model = Notebook
    context_object_name = "notebooks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_bar"] = set_nav()
        context["nav_bar_cards"] = set_nav_cards()
        context["current_page"] = "NOTEBOOKS"
        context["in_cart"] = in_basket(self.request)
        return context
    
class CardsView(ListView):
    template_name = "holmescraftsuk/cards.html"
    model = Card
    context_object_name = "cards"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_bar"] = set_nav()
        context["nav_bar_cards"] = set_nav_cards()
        context["current_page"] = get_object_or_404(Navbar, slug=self.kwargs["slug"])
        context["in_cart"] = in_basket(self.request)
        return context
    
class NotebookShopPageView(DetailView):
    template_name = "holmescraftsuk/notebook_shop_page.html" 
    model = Notebook 
    context_object_name = "notebook"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nav_bar"] = set_nav()
        context["nav_bar_cards"] = set_nav_cards()
        context["in_cart"] = in_basket(self.request)
        return context
    
    def post(self, request):
        cart = request.session.get("cart", {})
        product_id = request.POST["product_id"]
        quantity = request.POST["quantity"]

        cart[product_id] = quantity

        request.session["cart"] = cart
    
class CardShopPageView(DetailView):
    template_name = "holmescraftsuk/card_shop_page.html" 
    model = Card
    context_object_name = "card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context["nav_bar"] = set_nav()
        context["nav_bar_cards"] = set_nav_cards()
        context["in_cart"] = in_basket(self.request)
        return context 
    
    def post(self, request):
        cart = request.session.get("cart", {})
        product_id = request.POST["product_id"]
        quantity = request.POST["quantity"]

        cart[product_id] = quantity

        request.session["cart"] = cart
