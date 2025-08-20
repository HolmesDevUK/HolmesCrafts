from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.BasketView.as_view(), name="basket"),
    path("remove/", views.BasketRemoveView.as_view(), name="basket_remove"),
]
