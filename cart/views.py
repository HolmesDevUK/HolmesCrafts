from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from catalog.models import Product
from .models import CartItem
from .utils import get_cart


def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.Post.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart.item.quantity += qty
    else:
        cart_item.quantity = qty
    cart_item.save()

    return redirect("basket")

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect("basket")      

class BasketView(TemplateView):
    template_name = "cart/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)
        context["cart"] = cart
        context["items"] = cart.items.all()
        return context
    