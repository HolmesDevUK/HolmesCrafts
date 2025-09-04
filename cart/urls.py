from django.urls import path
from .views import BasketView, add_to_cart, update_cart_item, remove_from_cart

app_name = "cart"

urlpatterns = [
    path("", BasketView.as_view(), name="basket"),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-ajax/', update_cart_item, name='update_cart_ajax'),
    path('remove-ajax/<int:item_id>/', remove_from_cart, name='remove_cart_ajax'),
]
