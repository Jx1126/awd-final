from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
  class Meta:
    model = Course
    field = ['course_title', 'course_description']