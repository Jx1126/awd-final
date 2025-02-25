from django.db import models
from users.models import AppUser
import uuid
import os

def generate_uuid(instance, file):
  extension = file.split('.')[-1]
  file_uuid = f'{uuid.uuid4()}.{extension}'
  return os.path.join('course_materials/', file_uuid)

class Course(models.Model):
  course_title = models.CharField(max_length=150)
  course_description = models.TextField()
  created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='created_by')
  enrolled_students = models.ManyToManyField(AppUser, blank=True, related_name='enrolled_students')
  time_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.course_title
  
class CourseFeedback(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_feedbacks")
  student = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="student_feedbacks")
  feedback_content = models.TextField()
  time_submitted = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.student.user.username} left a feedback for {self.course.course_title}'
  
class CourseMaterial(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_materials")
  uploaded_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="uploaded_by")
  original_name = models.CharField(max_length=255, blank=True)
  title = models.CharField(max_length=150)
  file = models.FileField(upload_to=generate_uuid)
  upload_time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title