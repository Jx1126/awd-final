import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from users.models import AppUser


class ChatConsumer(AsyncWebsocketConsumer):
    # Connect to the chat room
    async def connect(self):
        # Get the room name from the URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # Create a group name
        self.room_group_name = "chat_%s" % self.room_name

        # Join the chat room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Accept the connection
        await self.accept()

    # Disconnect from the chat room
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive a message
    async def receive(self, text_data):
        # Get the message data
        text_data_json = json.loads(text_data)
        # Set the sender details and message
        message = text_data_json["message"]
        user = self.scope["user"]
        username = user.username
        # Wait for the sender's profile photo URL to be retrieved
        profile_photo_url = await self.get_profile_photo_url(user)
        time_sent = timezone.now().strftime("%d-%m-%Y %H:%M:%S ")

        # Send the message and sender details to the chat room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "profile_photo_url": profile_photo_url,
                "time_sent": time_sent,
            },
        )

    async def chat_message(self, event):
        # Get the message data
        message = event["message"]
        username = event["username"]
        profile_photo_url = event["profile_photo_url"]
        time_sent = event["time_sent"]

        # Send the message and sender details to the WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "profile_photo_url": profile_photo_url,
                    "time_sent": time_sent,
                }
            )
        )

    @sync_to_async
    # Get the sender's profile photo URL
    def get_profile_photo_url(self, user):
        try:
            app_user = AppUser.objects.get(user=user)
            return app_user.profile_photo.url
        except AppUser.DoesNotExist:
            return "/media/default_profile.jpg"
