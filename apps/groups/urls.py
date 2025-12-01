from django.urls import path
from .views import (
    GroupListCreateView,
    GroupRetrieveUpdateDestroyView,
    JoinGroupView,
    GroupMembersListView,
)

urlpatterns = [
    path("", GroupListCreateView.as_view(), name="group-list-create"),
    path("<int:pk>/", GroupRetrieveUpdateDestroyView.as_view(), name="group-detail"),
    path("<int:pk>/join/", JoinGroupView.as_view(), name="group-join"),
    path("<int:pk>/members/", GroupMembersListView.as_view(), name="group-members"),
]
