from django.db import models
from users.models import AppUser

class Course(models.Model):
  course_title = models.CharField(max_length=150)
  course_description = models.TextField()
  created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='created_by')
  enrolled_students = models.ManyToManyField(AppUser, blank=True, related_name='enrolled_students')
  time_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.course_title