from django.urls import path
from .views import BasketView, add_to_cart, remove_from_cart

app_name = "cart"

urlpatterns = [
    path("", BasketView.as_view(), name="basket"),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]
