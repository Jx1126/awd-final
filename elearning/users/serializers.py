from rest_framework import serializers
from .models import *

class UserStatusUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserStatusUpdate
    fields = ['id', 'user', 'status_content', 'time_posted']
    read_only_fields = ['id', 'time_posted']