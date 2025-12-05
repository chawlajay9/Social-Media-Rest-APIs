from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserListView,
    UserDetailView,
    RegisterView,
    RegisterView,
    CurrentUserView,
    LogoutView,
    ChangePasswordView,
)


urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # Auth
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path(
        "auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    # login
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "auth/logout/", LogoutView.as_view(), name="auth-logout"
    ),
    # POST with {"refresh": "<token>"}
    path("auth/me/", CurrentUserView.as_view(), name="auth-me"),
    path(
        "auth/change-password/",
        ChangePasswordView.as_view(),
        name="auth-change-password",
    ),
]
