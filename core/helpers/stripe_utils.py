import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404

from orders.models import Order

stripe.api_key = settings.STRIPE_SK

def get_or_create_stripe_product(product, product_image=None):
    if product.stripe_product_id:
        return product.stripe_product_id
    
    stripe_product = stripe.Product.create(
        name=product.name,
        description=product.description,
        images=[product_image] if product_image else None,
        metadata={"product_id": product.id},
    )

    product.stripe_product_id = stripe_product.id
    product.save(update_fields=["stripe_product_id"])

    return stripe_product.id

def get_or_create_stripe_price(product, unit_amount=None, currency="gdp", product_image=None):
    stripe_product_id = get_or_create_stripe_product(product, product_image=product_image)

    if unit_amount is None:
        unit_amount = product.price
    amount_cents = int(unit_amount * 100)

    if hasattr(product, "stripe_price_id") and product.stripe_price_id:
        return product.stripe_price_id

    stripe_price = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=amount_cents,
        currency=currency,
    ) 

    product.stripe_price_id = stripe_price.id
    product.save(update_fields=["stripe_price_id"])

    return stripe_price.id

def get_checkout_session_details(session_id: str):

    session = stripe.checkout.Session.retrieve(
        session_id,
        expand=["line_items", "customer_details"]
    )

    order = None
    order_id = session.metadata.get("order_id")
    if order_id:
        order = get_object_or_404(Order, id=order_id)

    customer_details = session.customer_details or {}
    address = customer_details.get("address", {})

    return {
        "session": session,
        "order": order,
        "customer": {
            "name": customer_details.get("name"),
            "email": customer_details.get("email"),
        },
        "shipping_address": {
            "line1": address.get("line1"),
            "line2": address.get("line2"),
            "city": address.get("city"),
            "state": address.get("state"),
            "postal_code": address.get("postal_code"),
            "country": address.get("country"),
        } if address else None,
        "line_items": session.line_items.data,
        "total_amount": session.amount_total / 100 if session.amount_total else None,
        "currency": session.currency.upper() if session.currency else None,
    }    
