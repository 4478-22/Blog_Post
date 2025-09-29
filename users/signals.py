from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, Follow, Notification
from .realtime import push_notification

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Follow)
def notify_follow(sender, instance: Follow, created, **kwargs):
    if not created:
        return
    if instance.follower_id == instance.following_id:
        return
    Notification.objects.create(
        recipient_id=instance.following_id,
        sender_id=instance.follower_id,
        notification_type=Notification.Type.FOLLOW,
        related_post=None,
    )
    push_notification(
        instance.following_id,
        {
            "type": "follow",
            "from_user_id": instance.follower_id,
            "created_at": instance.created_at.isoformat(),
        },
    )
