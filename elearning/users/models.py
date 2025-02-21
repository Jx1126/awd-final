from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  is_student = models.BooleanField(default=False)
  is_teacher = models.BooleanField(default=False)
  real_name = models.CharField(max_length=150)
  bio = models.TextField(blank=True)

class UserStatusUpdate(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_list')
  status_content = models.TextField()
  time_posted = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.real_name} at {self.time_posted}"