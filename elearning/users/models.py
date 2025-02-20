from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  is_student = models.BooleanField(default=False)
  is_teacher = models.BooleanField(default=False)
  real_name = models.CharField(max_length=150)
  bio = models.TextField(blank=True)