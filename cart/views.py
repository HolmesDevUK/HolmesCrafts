from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import CartItem
from .utils import get_cart


def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get("quantity", 1))
    chosen_img_url = request.POST.get("chosen_image")

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += qty
    else:
        cart_item.quantity = qty

    if chosen_img_url:
        cart_item.chosen_image = chosen_img_url    
    cart_item.save()

    return redirect("cart:basket")

@require_POST
def update_cart_item(request, item_id=None):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
    else:
        quantity = int(request.POST.get('quantity', 1))

    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity = quantity
    cart_item.save()

    if is_ajax:
        subtotal = cart_item.total_price()
        total = sum(item.total_price() for item in cart_item.cart.items.all())
        return JsonResponse({'subtotal': subtotal, 'total': total})

    return redirect('cart:basket')

@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        total = sum(item.total_price for item in cart.items.all())
        return JsonResponse({'total': total})

    return redirect('cart:basket') 

class BasketView(TemplateView):
    template_name = "cart/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)
        context["cart"] = cart
        context["items"] = cart.items.all()
        return context
    