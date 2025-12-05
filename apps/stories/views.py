from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import Story, StoryView
from .serializers import StorySerializer, StoryViewSerializer


class StoryCreateAPI(generics.CreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoryListAPI(generics.ListAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()

        # Auto remove expired stories
        Story.objects.filter(created_at__lt=now - timedelta(hours=24)).delete()

        user = self.request.user

        return (
            Story.objects.filter(
                # Public stories
                privacy="public"
            )
            | Story.objects.filter(
                # User's own stories
                user=user
            )
            | Story.objects.filter(
                # Friends' stories (logic simplified)
                privacy="friends",
                user__in=user.profile.friends.all(),
            )
        )


class StoryDetailAPI(generics.RetrieveAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]


class StoryViewAPI(generics.CreateAPIView):
    serializer_class = StoryViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        story_id = self.kwargs["story_id"]
        serializer.save(viewer=self.request.user, story_id=story_id)
