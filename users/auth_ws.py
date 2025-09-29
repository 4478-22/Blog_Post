# Simple JWT auth for Channels connections via ?token=...
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]
        scope["user"] = AnonymousUser()
        if token:
            try:
                payload = UntypedToken(token)
                user_id = payload.get("user_id") or payload.get("user")
                if user_id:
                    scope["user"] = await get_user(user_id)
            except (InvalidToken, TokenError):
                pass
        return await super().__call__(scope, receive, send)
