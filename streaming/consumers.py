import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"stream_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # Notify others that peer left
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "signal_message", "message": json.dumps({"type": "peer-left"})},
        )

    async def receive(self, text_data):
        # Forward any WebRTC signaling message (offer, answer, candidate) to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "signal_message", "message": text_data, "sender": self.channel_name},
        )

    async def signal_message(self, event):
        # Don't echo back to sender
        if event.get("sender") == self.channel_name:
            return
        await self.send(text_data=event["message"])
