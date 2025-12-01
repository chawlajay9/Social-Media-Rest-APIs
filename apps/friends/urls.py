from django.urls import path
from .views import FriendRequestListCreateView, FriendshipListView

urlpatterns = [
    path("requests/", FriendRequestListCreateView.as_view(), name="friend-requests"),
    path("friends/", FriendshipListView.as_view(), name="friend-list"),
]
