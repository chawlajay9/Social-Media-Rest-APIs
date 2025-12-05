from django.urls import path
from .views import StoryCreateAPI, StoryListAPI, StoryDetailAPI, StoryViewAPI

urlpatterns = [
    path("create/", StoryCreateAPI.as_view(), name="create-story"),
    path("list/", StoryListAPI.as_view(), name="list-stories"),
    path("<int:pk>/", StoryDetailAPI.as_view(), name="story-detail"),
    path("<int:story_id>/view/", StoryViewAPI.as_view(), name="story-view"),
]
