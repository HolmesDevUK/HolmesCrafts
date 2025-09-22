import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

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
        total=cart.total_price,
        status="pending",
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            product_id=item.product.id,
            unit_price=item.product.price,
            quantity=item.quantity,
        )

    line_items = []
    currency = "gbp"
    for oi in order.items.all():
        unit_amount = int(oi.unit_price * 100)
        line_items.append({
            "price_data": {
                "currency": currency,
                "unit_amount": unit_amount,
                "product_data": {"name": oi.product_name},
            },
            "quantity": oi.quantity,
        })

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
    )

    order.stripe_session_id = session.id
    order.save()

    return JsonResponse({"sessionId": session.id})

