from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("notebooks/", views.NotebooksView.as_view(), name="notebooks"),
    path("<slug:slug>/", views.CardsView.as_view(), name="cards"),
    path("notebooks/<slug:slug>/", views.NotebookShopPageView.as_view(), name="notebook_shop_page"),
    path("<slug:page_slug>/<slug:slug>/", views.CardShopPageView.as_view(), name="card_shop_page")
]
