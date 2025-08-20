from django.shortcuts import render, redirect
from django.views import View
from decimal import Decimal

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
