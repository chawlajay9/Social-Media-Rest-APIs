from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_display = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor",
            "actor_display",
            "notif_type",
            "entity_id",
            "read_status",
            "created_at",
        ]
        read_only_fields = fields
