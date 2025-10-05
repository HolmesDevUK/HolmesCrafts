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
