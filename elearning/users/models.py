from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
import os

def generate_uuid(instance, file):
  extension = file.split('.')[-1]
  file_uuid = f'{uuid.uuid4()}.{extension}'
  return os.path.join('profile_photos/', file_uuid)

class AppUser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  is_student = models.BooleanField(default=False)
  is_teacher = models.BooleanField(default=False)
  real_name = models.CharField(max_length=150)
  bio = models.TextField(blank=True)
  profile_photo = models.ImageField(upload_to=generate_uuid, null=True, blank=True, default='default_profile.jpg')

  def get_photo_url(self):
    if self.profile_photo:
      return self.profile_photo.url
    else:
      return f"{settings.MEDIA_URL}default_profile.jpg"
    
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    from .tasks import process_profile_photos
    process_profile_photos.delay(self.id)

class UserStatusUpdate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_list')
  status_title = models.CharField(max_length=150, null=True, blank=True)
  status_content = models.TextField()
  time_posted = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.real_name} at {self.time_posted}"