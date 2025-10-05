import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SK

def get_or_create_stripe_product(product):
    if product.stripe_product_id:
        return product.stripe_product_id
    
    stripe_product = stripe.Product.create(
        name=product.name,
        description=product.description,
        images=[product.image_url] if product.image_url else None,
        metadata={"product_id": product.id},
    )

    product.stripe_product_id = stripe_product.id
    product.save(update_fields=["stripe_product_id"])

    return stripe_product.id

def get_or_create_stripe_price(product, unit_amount=None, currency="gdp"):
    stripe_product_id = get_or_create_stripe_product(product)

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
