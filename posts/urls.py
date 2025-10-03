from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, PostSearchView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),

    # Extra endpoints
    path("posts/feed/", FeedView.as_view(), name="feed"),
    path("posts/search/", PostSearchView.as_view(), name="search"),
]
