from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def push_notification(user_id: int, payload: dict):
    """
    Send a WS message to the user's personal group.
    """
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"user_{user_id}",
        {"type": "notify", "payload": payload},
    )
