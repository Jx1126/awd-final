from celery import shared_task
from .models import Course, CourseMaterial
from users.models import AppUser

# Process the course materials asynchronously using Celery
@shared_task
def process_course_materials(course_id, user_id, title, path):
  try:
    # Save the course materials information to the database
    course = Course.objects.get(id=course_id)
    user = AppUser.objects.get(id=user_id)
    course_materials = CourseMaterial.objects.filter(course=course, uploaded_by=user, title=title, file=path)
    course_materials.save()
  except Exception as e:
    return str(e)