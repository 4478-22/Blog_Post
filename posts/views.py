# posts/views.py
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef, Prefetch
from rest_framework import viewsets, permissions, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts.
    Extra actions: like, unlike.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None

        # Prefetch likes lightly to compute is_liked without an extra query per row
        likes_prefetch = Prefetch(
            "likes",
            queryset=Like.objects.only("id", "user_id", "post_id"),
            to_attr="_prefetched_likes",
        )

        qs = (
            Post.objects.all()
            .select_related("author", "author__profile")
            .prefetch_related(likes_prefetch)
            .annotate(
                likes_count=Count("likes", distinct=True),
                comments_count=Count("comments", distinct=True),
            )
            .order_by("-created_at")
        )

        if user:
            # Optional: add Exists subquery to speed up is_liked checks if you don’t use prefetch
            pass

        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="like",
    )
    def like(self, request, pk=None):
        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post)
        return Response({"detail": "liked"}, status=status.HTTP_201_CREATED)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="unlike",
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments (supports replies via parent).
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return (
            Comment.objects.all()
            .select_related("post", "user", "user__profile")
            .prefetch_related("replies")
            .order_by("created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedView(generics.ListAPIView):
    """
    Newsfeed: posts from users that the current user follows (most recent first).
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # If schema generator or anonymous user → return empty queryset
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Post.objects.none()

        user = self.request.user
        following_ids = user.following.values_list("id", flat=True)

        likes_prefetch = Prefetch(
            "likes",
            queryset=Like.objects.only("id", "user_id", "post_id"),
            to_attr="_prefetched_likes",
        )

        return (
            Post.objects.filter(author_id__in=following_ids)
            .select_related("author", "author__profile")
            .prefetch_related(likes_prefetch)
            .annotate(
                likes_count=Count("likes", distinct=True),
                comments_count=Count("comments", distinct=True),
            )
            .order_by("-created_at")
        )


from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from rest_framework.permissions import AllowAny
from rest_framework import generics

class PostSearchView(generics.ListAPIView):
    """
    Full-text search over Post.content with rank ordering.
    """
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Or IsAuthenticated if you prefer

    def get_queryset(self):
        q = (self.request.query_params.get("q") or "").strip()
        base = (
            Post.objects.select_related("author", "author__profile")
            .annotate(
                likes_count=Count("likes", distinct=True),
                comments_count=Count("comments", distinct=True),
            )
        )
        if not q:
            return base.none()

        vector = SearchVector("content", weight="A")
        query = SearchQuery(q)
        qs = (
            base.annotate(rank=SearchRank(vector, query))
            .filter(rank__gt=0.0)
            .order_by("-rank", "-created_at")
        )
        return qs
