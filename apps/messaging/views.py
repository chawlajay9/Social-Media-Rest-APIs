from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Q


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # If query param ?with=<user_id> is provided, return conversation with that user
        other = self.request.query_params.get("with")
        qs = Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by("-created_at")
        if other:
            qs = qs.filter(
                (Q(sender=self.request.user) & Q(receiver__id=other))
                | (Q(sender__id=other) & Q(receiver=self.request.user))
            )
        return qs

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
