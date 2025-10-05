import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from cart.utils import get_cart
from orders.models import Order, OrderItem

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
    
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=email,
        total=cart.total_price(),
        status="pending",
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            product_id=item.product.id,
            unit_price=item.product.price,
            quantity=item.quantity,
            product_image=item.display_image,
        )

    line_items = []
    currency = "gbp"
    for oi in order.items.all():
        unit_amount = int(Decimal(oi.unit_price) * 100)
        if unit_amount <= 0:
            return HttpResponseBadRequest("Invalid unit amount")
        
        line_items.append({
            "price_data": {
                "currency": currency,
                "unit_amount": unit_amount,
                "product_data": {
                    "name": oi.product_name,
                    "images": [oi.product_image] if oi.product_image else [],
                },
            },
            "quantity": oi.quantity,
        })

        if not line_items:
            return HttpResponseBadRequest("No items to charge")

    success_url = request.build_absolute_uri(reverse("payments:success")) + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(reverse("payments:cancel"))

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            customer_email=email,
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"order_id": str(order.id)},
        )
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)    

    order.stripe_session_id = session.id
    order.save()

    return JsonResponse({"sessionId": session.id})

def success(request):
    return render(request, "payments/success.html")

def cancel(request):
    return render(request, "payments/cancel.html")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature")
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"]["order_id"]

        try:
            order = Order.objects.get(id=order_id)
            order.status = "paid"
            order.save()
        except Order.DoesNotExist:
            return HttpResponseBadRequest("Order not found")    
        
    return JsonResponse({"status": "ok"})    

