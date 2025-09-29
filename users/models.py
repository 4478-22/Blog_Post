# users/models.py
from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user. Email unique; 'following' exposed via an explicit through table (Follow).
    """
    email = models.EmailField(unique=True)

    # Self-referential M2M (User follows other Users) via concrete Follow model.
    # user.following -> users this user follows
    # user.followers -> users who follow this user (reverse relation)
    following = models.ManyToManyField(
        "self",
        through="Follow",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )

    def __str__(self) -> str:  # pragma: no cover
        return self.username or self.email


class Follow(models.Model):
    """
    Directed follow relationship: follower -> following
    """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_relations",
        db_index=True,
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower_relations",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="uniq_follow_pair"
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F("following")),
                name="prevent_self_follow",
            ),
        ]
        indexes = [
            models.Index(fields=["follower", "created_at"]),
            models.Index(fields=["following", "created_at"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.follower} → {self.following}"


class Profile(models.Model):
    """
    One-to-one user profile.
    We store a Supabase storage path (e.g., 'avatars/<uuid>.jpg'), not a signed URL.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    avatar_path = models.CharField(
        max_length=512, blank=True, null=True, help_text="Supabase storage key/path"
    )
    bio = models.TextField(blank=True, default="")

    # Access followers/following via user.followers / user.following.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def avatar_url(self) -> str:
        """
        Return a signed URL (or empty string) for the stored avatar_path.
        """
        if not self.avatar_path:
            return ""
        # Lazy import to avoid import-time coupling
        try:
            from django.conf import settings as dj_settings
            from core.supabase_storage import create_signed_url
            bucket = getattr(dj_settings, "SUPABASE_AVATARS_BUCKET", "avatars")
            return create_signed_url(bucket=bucket, path=self.avatar_path)
        except Exception:
            return ""

    def __str__(self) -> str:  # pragma: no cover
        return f"Profile<{self.user_id}>"


class Notification(models.Model):
    """
    Optional: event notifications for like/comment/follow.
    """
    class Type(models.TextChoices):
        LIKE = "like", "Like"
        COMMENT = "comment", "Comment"
        FOLLOW = "follow", "Follow"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        db_index=True,
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
        db_index=True,
    )
    notification_type = models.CharField(max_length=16, choices=Type.choices)

    # Optional linkage to a post (e.g., for a like/comment)
    related_post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["recipient", "is_read", "created_at"]),
            models.Index(fields=["sender", "created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(recipient=models.F("sender")),
                name="prevent_self_notify",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        r = self.recipient.username if isinstance(self.recipient, User) else self.recipient_id
        s = self.sender.username if isinstance(self.sender, User) else self.sender_id
        return f"Notify<{self.notification_type}> {s} → {r}"
