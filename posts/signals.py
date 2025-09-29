from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Like
from users.models import Notification
from users.realtime import push_notification

@receiver(post_save, sender=Like)
def notify_like(sender, instance: Like, created, **kwargs):
    if not created:
        return
    if instance.post.author_id == instance.user_id:
        return  # skip self-like (if possible)
    Notification.objects.create(
        recipient_id=instance.post.author_id,
        sender_id=instance.user_id,
        notification_type=Notification.Type.LIKE,
        related_post_id=instance.post_id,
    )
    push_notification(
        instance.post.author_id,
        {
            "type": "like",
            "post_id": instance.post_id,
            "from_user_id": instance.user_id,
            "created_at": instance.created_at.isoformat(),
        },
    )

@receiver(post_save, sender=Comment)
def notify_comment(sender, instance: Comment, created, **kwargs):
    if not created:
        return
    if instance.post.author_id == instance.user_id:
        return
    Notification.objects.create(
        recipient_id=instance.post.author_id,
        sender_id=instance.user_id,
        notification_type=Notification.Type.COMMENT,
        related_post_id=instance.post_id,
    )
    push_notification(
        instance.post.author_id,
        {
            "type": "comment",
            "post_id": instance.post_id,
            "comment_id": instance.id,
            "from_user_id": instance.user_id,
            "created_at": instance.created_at.isoformat(),
        },
    )
