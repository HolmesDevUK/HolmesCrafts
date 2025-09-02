from django.db import models

from accounts.models import CustomUser
from catalog.models import Product
from core.utils import upload_to

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        owner = self.user.name if self.user else f"Session {self.session_key}"
        return f"Cart ({owner})"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    chosen_image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    @property
    def display_image(self):
        if self.chosen_image:
            return self.chosen_image.url
        return self.product.cart_image.url if self.product.cart_image else ''

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"   

# Create your models here.
