from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    CommentCreateView,
    ReactionCreateView,
)

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/comment/", CommentCreateView.as_view(), name="comment-create"),
    path("<int:pk>/react/", ReactionCreateView.as_view(), name="reaction-create"),
]
