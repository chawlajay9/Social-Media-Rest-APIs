from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, password_validation

from apps.privacy.models import PrivacySetting
from .models import User


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "bio",
            "profile_pic",
            "tokens",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        # optional: use Django's password validators
        password_validation.validate_password(data["password"], self.instance)
        return data

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # create default privacy settings if you use PrivacySetting model
        try:
            from .models import PrivacySetting

            PrivacySetting.objects.get_or_create(user=user)
        except Exception:
            pass
        return user

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_tokens(self, obj):
        return self.get_tokens_for_user(obj)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_pic", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, min_length=6)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
