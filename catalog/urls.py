from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView, CategoryBySlugView, CategoryToggleActiveView,
    ProductListCreateView, ProductDetailView, ProductToggleActiveView,
    StockMovementListCreateView,
)

category_urls = [
    path("category/", CategoryListCreateView.as_view()),
    path("category/<int:pk>", CategoryDetailView.as_view()),
    path("category/slug/<slug:slug>", CategoryBySlugView.as_view()),
    path("category/<int:pk>/toggle", CategoryToggleActiveView.as_view()),
]

product_urls = [
    path("product/", ProductListCreateView.as_view()),
    path("product/<int:pk>", ProductDetailView.as_view()),
    path("product/<int:pk>/toggle", ProductToggleActiveView.as_view()),
    path("product/<int:product_id>/stock-movements/", StockMovementListCreateView.as_view()),
]

urlpatterns = category_urls + product_urls
