from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Card, Notebook
from core.models import Navbar
from cart.forms import CartAddForm

class NotebooksView(ListView):
    template_name = "catalog/notebooks.html"
    model = Notebook
    context_object_name = "notebooks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "NOTEBOOKS"
        return context
    
class CardsView(ListView):
    template_name = "catalog/cards.html"
    model = Card
    context_object_name = "cards"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = get_object_or_404(Navbar, slug=self.kwargs["slug"])
        return context
    
class NotebookShopPageView(DetailView):
    template_name = "catalog/notebook_shop_page.html" 
    model = Notebook 
    context_object_name = "notebook"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartAddForm()
        return context
    
class CardShopPageView(DetailView):
    template_name = "catalog/card_shop_page.html" 
    model = Card
    context_object_name = "card"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartAddForm()
        return context
    
