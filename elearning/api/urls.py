from django.urls import path
from .views import *

urlpatterns = [
  path('user/profile/', UserProfileView.as_view(), name='user-profile-api'),
  path('user/status-updates/', UserStatusUpdateView.as_view(), name='user-status-updates-api'),
  path('user/enrolled-courses/', UserEnrolledCoursesView.as_view(), name='user-enrolled-courses-api'),
  path('user/created-courses/', UserCreatedCoursesView.as_view(), name='user-created-courses-api'),
  path('user/notifications/', UserNotificationView.as_view(), name='user-notifications-api'),

  path('course/<int:course_id>/feedback/', CourseFeedbackView.as_view(), name='course-feedback-api'),
  path('course/<int:course_id>/materials/', CourseMaterialView.as_view(), name='course-materials-api'),
]