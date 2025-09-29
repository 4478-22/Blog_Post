# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Profile, Follow, Notification

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("id", "username", "email", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "email")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "avatar_path", "updated_at")
    search_fields = ("user__username", "user__email")

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created_at")
    search_fields = ("follower__username", "following__username")
    list_filter = ("created_at",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "sender", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("recipient__username", "sender__username")
