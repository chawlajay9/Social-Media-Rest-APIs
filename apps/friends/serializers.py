from rest_framework import serializers
from .models import FriendRequest, Friendship

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "sender", "receiver", "status", "created_at"]


class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.StringRelatedField()

    class Meta:
        model = Friendship
        fields = ["id", "friend", "created_at"]
