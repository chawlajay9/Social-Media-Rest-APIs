from rest_framework import serializers
from .models import PrivacySetting


class PrivacySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacySetting
        fields = ["visibility", "message_privacy", "last_seen_visible"]
