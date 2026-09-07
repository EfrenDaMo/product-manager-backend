from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import MeView, ChangePasswordView

urlpatterns = [
    path("me", MeView.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("logout", TokenBlacklistView.as_view()),
    path("change-password", ChangePasswordView.as_view()),
]
