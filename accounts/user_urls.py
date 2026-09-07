from django.urls import path
from .views import UserListCreateView, UserDetailView, UserToggleActiveView

urlpatterns = [
    path("", UserListCreateView.as_view()),
    path("<int:pk>", UserDetailView.as_view()),
    path("<int:pk>/toggle", UserToggleActiveView.as_view()),
]
