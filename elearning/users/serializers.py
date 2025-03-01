from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AppUser, UserStatusUpdate

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email']

class AppUserSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  profile_photo_url = serializers.SerializerMethodField()

  class Meta:
    model = AppUser
    fields = ['user', 'real_name', 'bio', 'is_student', 'is_teacher', 'profile_photo_url']

  def get_profile_photo_url(self, obj):
    return obj.get_photo_url()
  
class UserStatusUpdateSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = UserStatusUpdate
    fields = ['user', 'status_title', 'status_content', 'time_posted']