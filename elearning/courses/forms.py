from django import forms
from .models import Course, CourseFeedback, CourseMaterial


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_title", "course_description"]


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ["feedback_content"]


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ["title", "file"]
