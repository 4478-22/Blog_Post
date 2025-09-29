# users/serializers.py
from __future__ import annotations
from typing import Any

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import Profile, Follow
from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ["bio", "avatar_path", "avatar_url", "created_at", "updated_at"]
        read_only_fields = ["avatar_url", "created_at", "updated_at"]

    def get_avatar_url(self, obj: Profile) -> str:
        return obj.avatar_url()


class UserPublicSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile", "followers_count", "following_count"]
        read_only_fields = ["id", "email", "followers_count", "following_count"]


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile"]

    def create(self, validated_data: dict[str, Any]) -> AbstractBaseUser:
        return User.objects.create_user(**validated_data)


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        following = attrs.get("following")
        request = self.context["request"]
        if following == request.user:
            raise serializers.ValidationError("You cannot follow yourself.")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["follower"] = request.user
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            # Unique constraint (already following) → idempotent success
            return Follow.objects.get(
                follower=request.user, following=validated_data["following"]
            )
