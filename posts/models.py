# posts/models.py
from __future__ import annotations

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    """
    Basic post with text and optional image stored in Supabase.
    Store storage key/path (e.g., 'posts/<uuid>.jpg'), not a signed URL.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        db_index=True,
    )
    content = models.TextField()
    image_path = models.CharField(
        max_length=512, blank=True, null=True, help_text="Supabase storage key/path"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author", "created_at"]),
        ]

    def image_url(self) -> str:
        """
        Return a signed URL (or empty string) for the stored image_path.
        """
        if not self.image_path:
            return ""
        try:
            from django.conf import settings as dj_settings
            from core.supabase_storage import create_signed_url
            bucket = getattr(dj_settings, "SUPABASE_POSTS_BUCKET", "posts")
            return create_signed_url(bucket=bucket, path=self.image_path)
        except Exception:
            return ""

    def __str__(self) -> str:  # pragma: no cover
        return f"Post<{self.id}> by {self.author_id}"


class Comment(models.Model):
    """
    Nested comments using self-referential parent FK for replies.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def is_reply(self) -> bool:
        return self.parent_id is not None

    def __str__(self) -> str:  # pragma: no cover
        return f"Comment<{self.id}> on Post<{self.post_id}>"


class Like(models.Model):
    """
    Explicit like model for user ↔ post with uniqueness and timestamp.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        db_index=True,
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="uniq_like_per_user_post"),
        ]
        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"Like u{self.user_id} ♥ p{self.post_id}"
