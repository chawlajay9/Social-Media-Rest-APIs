from django.urls import path
from .views import StoryListCreateView, StoryDetailView

urlpatterns = [
    path("", StoryListCreateView.as_view(), name="story-list-create"),
    path("<int:pk>/", StoryDetailView.as_view(), name="story-detail"),
]
