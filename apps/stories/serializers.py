from rest_framework import serializers
from .models import Story


class StorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Story
        fields = ["id", "user", "media_url", "created_at", "expires_at"]
        read_only_fields = ["id", "user", "created_at"]
