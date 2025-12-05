from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Notification(models.Model):

    NOTIF_TYPES = [
        ("reaction", "Reaction"),
        ("comment", "Comment"),
        ("friend_request", "Friend Request"),
        ("message", "Message"),
        ("story_view", "Story View"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="actor_notifications"
    )
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES)
    entity_id = models.PositiveIntegerField(null=True, blank=True)
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
