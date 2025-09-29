from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import NotificationsConsumer
from .auth_ws import JWTAuthMiddleware

websocket_urlpatterns = [
    re_path(r"^ws/notifications/$", JWTAuthMiddleware(AuthMiddlewareStack(
        URLRouter([re_path(r"^ws/notifications/$", NotificationsConsumer.as_asgi())])
    ))),
]
