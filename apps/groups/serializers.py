from rest_framework import serializers
from .models import Group, GroupMember
from django.contrib.auth import get_user_model

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "description", "privacy", "created_by", "created_at"]
        read_only_fields = ["created_by", "created_at"]


class GroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupMember
        fields = ["id", "group", "user", "role", "joined_at"]
        read_only_fields = ["id", "user", "joined_at"]
