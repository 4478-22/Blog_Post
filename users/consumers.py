from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    """
    Each authenticated user joins a personal group: user_<id>.
    Server sends events to that group on like/comment/follow.
    """

    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return
        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # handler that receives messages from group_send
    async def notify(self, event):
        # event: {"type": "notify", "payload": {...}}
        await self.send_json(event.get("payload", {}))
