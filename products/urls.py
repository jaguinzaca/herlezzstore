from django.urls import path

from .views import catalog_view


app_name = "products"

urlpatterns = [
    path("", catalog_view, name="catalog"),
]
