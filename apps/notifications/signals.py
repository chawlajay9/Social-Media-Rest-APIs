from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from notifications.models import Notification
from posts.models import Reaction, Comment
from messages.models import Message
from friends.models import FriendRequest
from stories.models import StoryView


def create_notif(user, actor, notif_type, entity_id=None):
    if user == actor:
        return

    Notification.objects.create(
        user=user,
        actor=actor,
        notif_type=notif_type,
        entity_id=entity_id or 0,
    )


# 📌 Reaction → Notification
@receiver(post_save, sender=Reaction)
def notify_reaction(sender, instance, created, **kwargs):
    if created:
        create_notif(
            user=instance.post.user,
            actor=instance.user,
            notif_type="reaction",
            entity_id=instance.post.id,
        )


# 📌 Comment → Notification
@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created:
        create_notif(
            user=instance.post.user,
            actor=instance.user,
            notif_type="comment",
            entity_id=instance.post.id,
        )


# 📌 Messages → Notification
@receiver(post_save, sender=Message)
def notify_message(sender, instance, created, **kwargs):
    if created:
        create_notif(
            user=instance.receiver,
            actor=instance.sender,
            notif_type="message",
            entity_id=instance.id,
        )


# 📌 Friend Request → Notification
@receiver(post_save, sender=FriendRequest)
def notify_friend_request(sender, instance, created, **kwargs):
    if created:
        create_notif(
            user=instance.receiver,
            actor=instance.sender,
            notif_type="friend_request",
            entity_id=instance.id,
        )


# 📌 Story View → Notification
@receiver(post_save, sender=StoryView)
def notify_story_view(sender, instance, created, **kwargs):
    if created:
        create_notif(
            user=instance.story.user,
            actor=instance.viewer,
            notif_type="story_view",
            entity_id=instance.story.id,
        )
