from django.urls import path
from . import views

urlpatterns = [
     path("", views.HomeView.as_view(), name="home_page"),
     path("notebooks", views.NotebooksView.as_view(), name="notebooks"),
     path("basket", views.BasketView.as_view(), name="basket"),
     path("checkout", views.CheckoutView.as_view(), name="checkout"),
     path("success", views.SuccessView.as_view(), name="success"), 
     path("basket/remove", views.BasketRemoveView.as_view(), name="basket_remove"),
     path("<slug:slug>", views.CardsView.as_view(), name="cards"),
     path("notebooks/<slug:slug>", views.NotebookShopPageView.as_view(), name="notebook_shop_page"),
     path("<slug:page_slug>/<slug:slug>", views.CardShopPageView.as_view(), name="card_shop_page")
]