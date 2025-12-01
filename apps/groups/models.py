from django.db import models

from apps.core_users.models import User


# Create your models here.
class Group(models.Model):
    PRIVACY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
        ("secret", "Secret"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default="public")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class GroupMember(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("member", "Member"),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "user")
