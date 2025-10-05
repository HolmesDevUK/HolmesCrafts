from django.conf import settings
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_session_id = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} ({self.email or self.user}) - {self.status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    product_image = models.URLField(blank=True, null=True)

