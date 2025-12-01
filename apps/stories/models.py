from django.db import models

from apps.core_users.models import User


# Create your models here.
class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    media_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_active(self):
        from django.utils import timezone

        return timezone.now() < self.expires_at
