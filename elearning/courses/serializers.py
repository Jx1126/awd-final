from rest_framework import serializers
from .models import Course, CourseFeedback, CourseMaterial, Notification
from users.serializers import AppUserSerializer


class CourseSerializer(serializers.ModelSerializer):
    created_by = AppUserSerializer(read_only=True)
    enrolled_students = AppUserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "course_title",
            "course_description",
            "time_created",
            "created_by",
            "enrolled_students",
        ]


class CourseFeedbackSerializer(serializers.ModelSerializer):
    student = AppUserSerializer(read_only=True)

    class Meta:
        model = CourseFeedback
        fields = ["id", "course", "student", "feedback_content", "time_submitted"]


class CourseMaterialSerializer(serializers.ModelSerializer):
    uploaded_by = AppUserSerializer(read_only=True)

    class Meta:
        model = CourseMaterial
        fields = [
            "id",
            "course",
            "uploaded_by",
            "original_name",
            "title",
            "file",
            "upload_time",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    user = AppUserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "user", "message", "time_created", "read"]
