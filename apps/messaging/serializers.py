from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chat, Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "chat",
            "sender",
            "text",
            "media",
            "is_seen",
            "seen_at",
            "created_at",
        ]
        read_only_fields = ["id", "sender", "is_seen", "seen_at", "created_at"]


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "name",
            "participants",
            "is_group",
            "last_message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "last_message"]

    def get_last_message(self, chat):
        msg = chat.messages.last()
        return MessageSerializer(msg).data if msg else None
