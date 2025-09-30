# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse

from users.views import RegistrationView, UserViewSet
from posts.views import PostViewSet, CommentViewSet, FeedView, PostSearchView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Router for API endpoints
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

# Root landing view
def api_root(request):
    return JsonResponse({
        "message": "🚀 Welcome to the Social Blogging API",
        "version": "1.0.0",
        "endpoints": {
            "auth_register": "/api/auth/register/",
            "auth_jwt_create": "/api/auth/jwt/create/",
            "auth_jwt_refresh": "/api/auth/jwt/refresh/",
            "users": "/api/users/",
            "posts": "/api/posts/",
            "comments": "/api/comments/",
            "feed": "/api/feed/",
            "search_posts": "/api/posts/search/",
            "docs_swagger": "/api/docs/",
            "docs_redoc": "/api/redoc/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    # Root API landing page
    path("", api_root, name="api-root"),

    # Admin
    path("admin/", admin.site.urls),

    # Auth
    path("api/auth/register/", RegistrationView.as_view(), name="register"),
    path("api/auth/jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("api/auth/jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    # Core API
    path("api/", include(router.urls)),
    path("api/feed/", FeedView.as_view(), name="feed"),
    path("api/posts/search/", PostSearchView.as_view(), name="post-search"),

    # API Schema & Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
