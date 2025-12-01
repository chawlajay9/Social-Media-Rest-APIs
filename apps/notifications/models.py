from django.db import models

from apps.core_users.models import User


# Create your models here.
class Notification(models.Model):
    NOTIF_TYPE = [
        ("like", "Like"),
        ("comment", "Comment"),
        ("friend_request", "Friend Request"),
        ("message", "Message"),
        ("tag", "Tag"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="triggered_notifications"
    )
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE)
    entity_id = models.BigIntegerField()  # post_id, comment_id, etc.
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
