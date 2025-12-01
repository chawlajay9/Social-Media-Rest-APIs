from django.db import models
from apps.core_users.models import User

# Create your models here.
class PrivacySetting(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("friends", "Friends"),
        ("only_me", "Only Me"),
    ]
    MESSAGE_PRIVACY_CHOICES = [
        ("everyone", "Everyone"),
        ("friends", "Friends"),
        ("no_one", "No One"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="privacy")
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default="public"
    )
    message_privacy = models.CharField(
        max_length=10, choices=MESSAGE_PRIVACY_CHOICES, default="everyone"
    )
    last_seen_visible = models.BooleanField(default=True)
