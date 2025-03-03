from django.test import TestCase
from django.contrib.auth.models import User
from users.models import AppUser, UserStatusUpdate
from courses.models import Course, CourseMaterial, CourseFeedback, Notification
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

class TestAPI(TestCase):
  def setUp(self):
    # Create a student user
    self.student_user = User.objects.create_user(username='student_1', password='abcd')
    self.student_app_user = AppUser.objects.create(user=self.student_user, is_student=True, real_name='Student One', bio='Student One Bio')
    # Create a teacher user
    self.teacher_user = User.objects.create_user(username='teacher_1', password='abcd')
    self.teacher_app_user = AppUser.objects.create(user=self.teacher_user, is_teacher=True)
    # Create a course and enroll the student
    self.course = Course.objects.create(course_title='Test Course', course_description='Test Course Description', created_by=self.teacher_app_user)
    self.course.enrolled_students.add(self.student_app_user)
    self.course_feedback = CourseFeedback.objects.create(course=self.course, student=self.student_app_user, feedback_content="Test Feedback")
    # Create a course material
    self.test_course_materials = CourseMaterial.objects.create(course=self.course, uploaded_by=self.teacher_app_user, title='Test Material')
    # Create default status updates
    self.status_update = UserStatusUpdate.objects.create(user=self.student_user, status_title='Test Status', status_content='Test Status Content')
    self.status_update = UserStatusUpdate.objects.create(user=self.teacher_user, status_title='Test Status', status_content='Test Status Content')
    # Create a notification
    self.notification = Notification.objects.create(user=self.student_app_user, message='Test Notification Message')
    # Create an API client
    self.client = APIClient()

  # API Test 1: Users can retrieve their profile information
  def test_user_profile_api(self):
    # Force authenticate as a student
    self.client.force_authenticate(user=self.student_user)
    # Retrieve the user profile information
    response = self.client.get('/api/user/profile/')
    self.assertEqual(response.status_code, 200)
    # Check if the profile information can be retrieved
    self.assertEqual(response.data['user']['username'], 'student_1')
    self.assertEqual(response.data['real_name'], 'Student One')

  # API Test 2: Users can retrieve their status updates
  def test_user_status_updates_api(self):
    # Force authenticate as a student
    self.client.force_authenticate(user=self.student_user)
    # Retrieve the user status updates
    response = self.client.get('/api/user/status-updates/')
    self.assertEqual(response.status_code, 200)
    # Check if the status can be retrieved
    self.assertEqual(response.data[0]['status_title'], 'Test Status')
    self.assertEqual(response.data[0]['status_content'], 'Test Status Content')

  # API Test 3: Students can retrieve their enrolled courses
  def test_user_enrolled_courses_api(self):
    # Force authenticate as a student
    self.client.force_authenticate(user=self.student_user)
    # Retrieve the user enrolled courses
    response = self.client.get('/api/user/enrolled-courses/')
    self.assertEqual(response.status_code, 200)
    # Check if the enrolled courses can be retrieved
    self.assertEqual(response.data[0]['course_title'], 'Test Course')
    self.assertEqual(response.data[0]['course_description'], 'Test Course Description')
    self.assertEqual(response.data[0]['created_by']['user']['username'], 'teacher_1')

  # API Test 5: Users can retrieve their notifications
  def test_user_notifications_api(self):
    # Force authenticate as a student
    self.client.force_authenticate(user=self.student_user)
    # Retrieve the user notifications
    response = self.client.get('/api/user/notifications/')
    self.assertEqual(response.status_code, 200)
    # Check if the notifications can be retrieved
    self.assertEqual(response.data[0]['message'], 'Test Notification Message')

  # API Test 6: Teachers can retrieve their created courses
  def test_user_created_courses_api(self):
    # Force authenticate as a teacher
    self.client.force_authenticate(user=self.teacher_user)
    # Retrieve the user created courses
    response = self.client.get('/api/user/created-courses/')
    self.assertEqual(response.status_code, 200)
    # Check if the created courses can be retrieved
    self.assertEqual(response.data[0]['course_title'], 'Test Course')
    self.assertEqual(response.data[0]['course_description'], 'Test Course Description')

  # API Test 7: Users can retrieve course feedback
  def test_course_feedback_api(self):
    # Force authenticate as a student
    self.client.force_authenticate(user=self.student_user)
    # Retrieve the course feedback
    response = self.client.get('/api/course/1/feedback/')
    self.assertEqual(response.status_code, 200)
    # Check if the course feedback can be retrieved
    self.assertEqual(response.data[0]['student']['user']['username'], 'student_1')
    self.assertEqual(response.data[0]['feedback_content'], 'Test Feedback')

  # API Test 8: Users can retrieve course materials
  def test_course_materials_api(self):
    # Force authenticate as a student
    self.client.force_authenticate(user=self.student_user)
    # Retrieve the course materials
    response = self.client.get('/api/course/1/materials/')
    self.assertEqual(response.status_code, 200)
    # Check if the course materials can be retrieved
    self.assertEqual(response.data[0]['title'], 'Test Material')