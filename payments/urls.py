from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("success/", views.SuccessView.as_view(), name="success")
]
