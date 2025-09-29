# users/views.py
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow
from .serializers import (
    RegistrationSerializer,
    UserPublicSerializer,
    FollowSerializer,
)

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    """
    Public endpoint to register a user.
    Login is handled by SimpleJWT (/api/auth/jwt/create).
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public read endpoints for users; includes follower/following counts.
    Authenticated-only actions: follow/unfollow, me.
    """
    queryset = (
        User.objects.all()
        .annotate(
            followers_count=Count("followers", distinct=True),
            following_count=Count("following", distinct=True),
        )
        .select_related()
    )
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=["get"], detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = (
            User.objects.filter(pk=request.user.pk)
            .annotate(
                followers_count=Count("followers", distinct=True),
                following_count=Count("following", distinct=True),
            )
            .first()
        )
        return Response(self.get_serializer(user).data)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="follow",
    )
    def follow(self, request, pk=None):
        target = self.get_object()
        serializer = FollowSerializer(
            data={"following": target.pk}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        follow_obj = serializer.save()
        return Response(FollowSerializer(follow_obj).data, status=status.HTTP_201_CREATED)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="unfollow",
    )
    def unfollow(self, request, pk=None):
        target = self.get_object()
        deleted, _ = Follow.objects.filter(
            follower=request.user, following=target
        ).delete()
        # idempotent: return 204 whether or not it existed
        return Response(status=status.HTTP_204_NO_CONTENT)
