from rest_framework import generics, permissions
from users.models import AppUser, UserStatusUpdate
from users.serializers import AppUserSerializer, UserStatusUpdateSerializer
from courses.models import Course, CourseFeedback, CourseMaterial, Notification
from courses.serializers import (
    CourseSerializer,
    CourseFeedbackSerializer,
    CourseMaterialSerializer,
    NotificationSerializer,
)
from .permissions import IsTeacher, IsStudent


# Retrieve the user profile information
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppUserSerializer

    def get_object(self):
        return AppUser.objects.get(user=self.request.user)


# Retrieve the user status updates
class UserStatusUpdateView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserStatusUpdateSerializer

    def get_queryset(self):
        return UserStatusUpdate.objects.filter(user=self.request.user).order_by(
            "-time_posted"
        )


class UserEnrolledCoursesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = CourseSerializer

    def get_queryset(self):
        app_user = AppUser.objects.get(user=self.request.user)
        return Course.objects.filter(enrolled_students=app_user).order_by(
            "-time_created"
        )


class UserNotificationView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        app_user = AppUser.objects.get(user=self.request.user)
        return Notification.objects.filter(user=app_user).order_by("-time_created")


class UserCreatedCoursesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    serializer_class = CourseSerializer

    def get_queryset(self):
        app_user = AppUser.objects.get(user=self.request.user)
        return Course.objects.filter(created_by=app_user).order_by("-time_created")


class CourseFeedbackView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseFeedbackSerializer

    def get_queryset(self):
        app_user = AppUser.objects.get(user=self.request.user)
        course_id = self.kwargs["course_id"]

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return CourseFeedback.objects.none()

        if app_user.is_student:
            return CourseFeedback.objects.filter(course=course).order_by(
                "-time_submitted"
            )
        elif app_user.is_teacher and course.created_by == app_user:
            return CourseFeedback.objects.filter(course=course).order_by(
                "-time_submitted"
            )

        return CourseFeedback.objects.none()


class CourseMaterialView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseMaterialSerializer

    def get_queryset(self):
        app_user = AppUser.objects.get(user=self.request.user)
        course_id = self.kwargs["course_id"]

        if app_user.is_student:
            return CourseMaterial.objects.filter(
                course__id=course_id, course__enrolled_students=app_user
            ).order_by("-upload_time")
        elif app_user.is_teacher:
            return CourseMaterial.objects.filter(
                course__id=course_id, course__created_by=app_user
            ).order_by("-upload_time")
