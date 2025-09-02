from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'display_subtotal', 'chosen_image_display')

    def display_subtotal(self, obj):
        return obj.subtotal
    display_subtotal.short_description = "Subtotal"

    def chosen_image_display(self, obj):
        if obj.chosen_image:
            return f"<img src='{obj.chosen_image.url}' style='height:50px;' />"
        elif obj.product and hasattr(obj.product, 'cart_image') and obj.product.cart_image:
            return f"<img src='{obj.product.cart_image.url}' style='height:50px;' />"
        return "-"
    chosen_image_display.allow_tags = True
    chosen_image_display.short_description = "Image"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'display_total_items', 'display_total_price', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'display_total_items', 'display_total_price')
    inlines = [CartItemInline]
    list_filter = ('created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'session_key')

    def display_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    display_total_items.short_description = "Total Items"

    def display_total_price(self, obj):
        return sum(item.subtotal for item in obj.items.all())
    display_total_price.short_description = "Total Price"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'display_subtotal')
    readonly_fields = ('display_subtotal',)
    search_fields = ('product__name',)

    def display_subtotal(self, obj):
        return obj.subtotal
    display_subtotal.short_description = "Subtotal"
