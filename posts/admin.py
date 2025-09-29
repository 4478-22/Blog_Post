# posts/admin.py
from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")
    search_fields = ("author__username", "content")
    list_filter = ("created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "parent", "created_at")
    search_fields = ("user__username", "post__id", "content")
    list_filter = ("created_at",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    search_fields = ("user__username", "post__id")
    list_filter = ("created_at",)
