from rest_framework import generics, permissions
from django.utils import timezone
from .models import Story
from .serializers import StorySerializer


class StoryListCreateView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return only active stories
        now = timezone.now()
        return Story.objects.filter(expires_at__gt=now).order_by("-created_at")

    def perform_create(self, serializer):
        # set creator and default expiry to 24 hours if not provided
        expires_at = serializer.validated_data.get("expires_at")
        if not expires_at:
            expires_at = timezone.now() + timezone.timedelta(hours=24)
        serializer.save(user=self.request.user, expires_at=expires_at)


class StoryDetailView(generics.RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]
