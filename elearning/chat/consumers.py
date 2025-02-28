import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from users.models import AppUser
class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name
    
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    user = self.scope['user']
    username = user.username
    profile_photo_url = await self.get_profile_photo_url(user)
    time_sent = timezone.now().strftime('%d-%m-%Y %H:%M:%S ')

    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'username': username,
        'profile_photo_url': profile_photo_url,
        'time_sent': time_sent
      }
    )

  async def chat_message(self, event):
    message = event['message']
    username = event['username']
    profile_photo_url = event['profile_photo_url']
    time_sent = event['time_sent']

    await self.send(text_data=json.dumps({
      'message': message,
      'username': username,
      'profile_photo_url': profile_photo_url,
      'time_sent': time_sent
    }))

  @sync_to_async
  def get_profile_photo_url(self, user):
    try:
      app_user = AppUser.objects.get(user=user)
      return app_user.profile_photo.url
    except AppUser.DoesNotExist:
      return "/media/default_profile.jpg"