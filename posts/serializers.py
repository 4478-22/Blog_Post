# posts/serializers.py
from __future__ import annotations
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserPublicSerializer
from .models import Post, Comment, Like

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "image_path",
            "image_url",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "is_liked",
        ]
        read_only_fields = [
            "id",
            "author",
            "image_url",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "is_liked",
        ]

    def get_image_url(self, obj: Post) -> str:
        return obj.image_url()

    def get_is_liked(self, obj: Post) -> bool:
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        # Prefetched in views; fall back gracefully
        return any(l.user_id == user.id for l in getattr(obj, "_prefetched_likes", []))


class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    is_reply = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "user", "content", "parent", "is_reply", "created_at"]
        read_only_fields = ["id", "user", "is_reply", "created_at"]

    def get_is_reply(self, obj: Comment) -> bool:
        return obj.parent_id is not None

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        parent = attrs.get("parent")
        post = attrs.get("post") or getattr(self.instance, "post", None)
        if parent and post and parent.post_id != post.id:
            raise serializers.ValidationError("Parent comment must belong to the same post.")
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
