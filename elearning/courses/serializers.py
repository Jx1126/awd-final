from rest_framework import serializers
from .models import Course
from users.models import AppUser

class CourseSerializer(serializers.ModelSerializer):
  created_by = serializers.StringRelatedField()
  enrolled_students = serializers.StringRelatedField(many=True)

  class Meta:
    model = Course
    field = ['id', 'course_title', 'course_description', 'created_by', 'enrolled_students', 'time_created']