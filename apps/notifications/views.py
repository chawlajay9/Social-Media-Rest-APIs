from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ids = request.data.get("ids", [])

        if ids:
            qs = Notification.objects.filter(user=request.user, id__in=ids)
            qs.update(read_status=True)
            return Response({"marked": qs.count()})

        if request.data.get("all"):
            qs = Notification.objects.filter(user=request.user, read_status=False)
            count = qs.count()
            qs.update(read_status=True)
            return Response({"marked_all": count})

        return Response({"error": "specify ids or all"})


class UnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            user=request.user, read_status=False
        ).count()
        return Response({"unread_count": count})
