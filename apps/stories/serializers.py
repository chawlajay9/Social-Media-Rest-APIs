from rest_framework import serializers
from .models import Story, StoryView


class StorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    views_count = serializers.IntegerField(source="views.count", read_only=True)

    class Meta:
        model = Story
        fields = "__all__"
        read_only_fields = ("user",)


class StoryViewSerializer(serializers.ModelSerializer):
    viewer = serializers.StringRelatedField()

    class Meta:
        model = StoryView
        fields = "__all__"
