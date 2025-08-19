from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from decimal import Decimal
import os
from dotenv import load_dotenv
import stripe

from .models import Notebook, Card, Navbar

# Create your views here.

load_dotenv()

stripe_pk = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe_sk = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = stripe_sk

def in_basket(request):
    cart = request.session.get("cart", {})
    quantities_list = []

    for product_code, product in cart.items():
        quantity = product["quantity"]
        quantities_list.append(quantity)

    in_cart = sum(quantities_list)    
    
    return in_cart

def set_nav():
    nav_bar = Navbar.objects.filter(is_card=False)

    return nav_bar

def set_nav_cards():
    nav_bar_cards = Navbar.objects.filter(is_card=True)

    return nav_bar_cards


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
    
class BasketView(View):
    def order_total(self, request):
        cart = request.session.get("cart", {})
        order_totals = []

        for product_code, product in cart.items():
            total = Decimal(product["total"])
            order_totals.append(total)

        order_total = sum(order_totals)

        if order_total:
            return order_total    
          

    def get(self, request):
        cart = request.session.get("cart", {})

        if cart == {}:
            basket_empty = True
        else:
            basket_empty = False    

        context = {
            "nav_bar": set_nav(),
            "nav_bar_cards": set_nav_cards(),
            "cart": cart,
            "basket_empty": basket_empty,
            "in_cart": in_basket(self.request),
            "order_total": self.order_total(self.request)
        }

        return render(request, "holmescraftsuk/basket.html", context)
    
    def post(self, request):
        cart = request.session.get("cart", {})
        product_code = request.POST["product_code"]
        quantity = int(request.POST["quantity"])
        product_img = request.POST["product_img"]
        product_name = request.POST["product_name"]
        product_price = request.POST["product_price"]

        cart[product_code] = cart.get(product_code, {})
        cart[product_code]["image"] = product_img
        cart[product_code]["name"] = product_name
        cart[product_code]["price"] = product_price
        cart[product_code]["quantity"] = cart[product_code].get("quantity", 0) + quantity
        total = Decimal(cart[product_code].get("price", 0)) * Decimal(cart[product_code].get("quantity", 0))
        cart[product_code]["total"] = str(total)

        request.session["cart"] = cart

        return redirect("home_page")
    
class BasketRemoveView(View):
    def post(self, request):
            cart = request.session.get("cart", {})
            product_code = request.POST["product_code"]

            del cart[product_code]

            request.session["cart_notebooks"] = cart

            return redirect("basket")  
    
class CheckoutView(View):
    def post(self, request):
        line_items = []
        cart = request.session.get("cart", {})
        for product_code, product in cart.items():
            price = Decimal(product["price"]) * 100
            line_item = {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": product["name"],
                        # "images": [product["image"]],
                    },
                    "unit_amount": int(price),
                },
                "quantity": product["quantity"],
            }

            line_items.append(line_item)


        session = stripe.checkout.Session.create(
            line_items = line_items,
            mode = "payment",
            success_url="http://127.0.0.1:8000/success",
            cancel_url="http://127.0.0.1:8000/cancel",
        )  

        return redirect(session.url, code=303)
    
class SuccessView(View):
    def get(self, request):
        del request.session["cart"]

        context = {
            "nav_bar": set_nav(),
            "nav_bar_cards": set_nav_cards(),
            "in_cart": in_basket(self.request),
        }
        
        return render(request, "holmescraftsuk/success.html", context)
        


    

    

    

    
