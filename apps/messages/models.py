from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    """
    A chat can be:
    - one-to-one (is_group=False)
    - group chat (is_group=True)
    """

    name = models.CharField(max_length=255, blank=True)  # only for groups
    participants = models.ManyToManyField(User, related_name="chats")
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_group:
            return f"Group: {self.name}"
        return f"Chat {self.id}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    text = models.TextField(blank=True)
    media = models.FileField(upload_to="messages/media/", blank=True, null=True)

    is_seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message {self.id} in Chat {self.chat.id}"
