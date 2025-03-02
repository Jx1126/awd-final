from django.urls import path
from .views import *
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
  path('schema/', get_schema_view(title="eLearning Application", description="API that allows users to access their data", version="1.0"), name='openapi_schema'),
  path('swagger/', TemplateView.as_view(template_name='swagger.html', extra_context={'schema_url': 'openapi_schema'}), name='swagger_ui'),

  path('user/profile/', UserProfileView.as_view(), name='user_profile_api'),
  path('user/status-updates/', UserStatusUpdateView.as_view(), name='user_status_updates_api'),
  path('user/enrolled-courses/', UserEnrolledCoursesView.as_view(), name='user_enrolled_courses_api'),
  path('user/created-courses/', UserCreatedCoursesView.as_view(), name='user_created_courses_api'),
  path('user/notifications/', UserNotificationView.as_view(), name='user_notifications_api'),

  path('course/<int:course_id>/feedback/', CourseFeedbackView.as_view(), name='course_feedback_api'),
  path('course/<int:course_id>/materials/', CourseMaterialView.as_view(), name='course_materials_api'),
]