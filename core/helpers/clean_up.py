from datetime import timedelta
from django.utils import timezone

from cart.models import Cart

def delete_old_carts(days=7):

    cutoff_date = timezone.now() - timedelta(days=days)
    old_carts = Cart.objects.filter(user__isnull=True, updated_at__lt=cutoff_date)
    count = old_carts.count()
    old_carts.delete()
    return count