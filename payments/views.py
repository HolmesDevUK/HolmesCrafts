from django.shortcuts import render, redirect
from django.views import View
from decimal import Decimal
import stripe
import environ

env = environ.Env()

stripe_pk = env("STRIPE_PUBLISHABLE_KEY")
stripe_sk = env("STRIPE_SECRET_KEY")
stripe.api_key = stripe_sk

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