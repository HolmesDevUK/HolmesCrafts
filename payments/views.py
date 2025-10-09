import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import traceback

from cart.utils import get_cart
from orders.models import Order, OrderItem
from core.utils import absolute_url
from core.helpers.stripe_utils import get_or_create_stripe_price, get_checkout_session_details
from core.helpers.email_utils import order_confirmation_admin

stripe.api_key = settings.STRIPE_SK

@require_POST
def create_order_and_checkout_session(request):
    cart = get_cart(request)
    if not cart.items.exists():
        return HttpResponseBadRequest("Cart empty")
    
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = request.POST.get("email")
        if not email:
            return HttpResponseBadRequest("Guest email required")    
    
    try:
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email,
            total=cart.total_price(),
            status="pending",
        )

        line_items = []

        for item in cart.items.all():
            order_image = absolute_url(item.display_image, request)

            if settings.PLACEHOLDER_IMAGE:
                order_image = settings.PLACEHOLDER_IMAGE


            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_id=item.product.id,
                unit_price=item.product.price,
                quantity=item.quantity,
                product_image=order_image,
            )

            stripe_price_id = get_or_create_stripe_price(item.product, unit_amount=item.product.price, currency="gbp", product_image=order_image)

        
        
            
            line_items.append({
                "price": stripe_price_id,
                "quantity": item.quantity,
            })

        if not line_items:
            return HttpResponseBadRequest("No items to charge")

        success_url = request.build_absolute_uri(reverse("payments:success")) + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = request.build_absolute_uri(reverse("payments:cancel"))

        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            customer_email=email,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"order_id": str(order.id)},
            shipping_address_collection={
                "allowed_countries": ["GB", "US", "CA"],
            },
        )  

        order.stripe_session_id = session.id
        order.save()

        return JsonResponse({"sessionId": session.id})
    
    except stripe.error.StripeError as e:
        print("❌ Stripe error:", e)
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        print("❌ Unexpected error:", e)
        traceback.print_exc()
        return JsonResponse({"error": "Something went wrong: " + str(e)}, status=500)

def success(request):
    return render(request, "payments/success.html")

def cancel(request):
    return render(request, "payments/cancel.html")

@csrf_exempt
def stripe_webhook(request):
    print("🔔 Webhook received!")
    
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature:", e)
        return HttpResponseBadRequest("Invalid signature")
    except stripe.error.StripeError as e:
        print("Stripe API error:", e)
        return HttpResponseServerError("Stripe API error")
    except Exception as e:
        print("Unexpected error:", e)
        return HttpResponseServerError("Something went wrong")
    
    print("Received event:", event["type"])
    print(event)
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        
        data = get_checkout_session_details(session_id)

        order = data["order"]
        if order:
            order.status = "paid"
            order.save()

        order_confirmation_admin(data)    
        
    return JsonResponse({"status": "ok"})    

