from django.test import TestCase
from django.contrib.auth.models import User
from users.models import AppUser, UserStatusUpdate
from courses.models import Course, CourseFeedback, Notification
from django.core.files.uploadedfile import SimpleUploadedFile

class TestUser(TestCase):
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
    # Create default status updates
    self.status_update = UserStatusUpdate.objects.create(user=self.student_user, status_title='Test Status', status_content='Test Status Content')
    self.status_update = UserStatusUpdate.objects.create(user=self.teacher_user, status_title='Test Status', status_content='Test Status Content')
    
  # User Test 1: Homepage loads with corresponding data for users
  def test_homepage_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # Load the homepage
    response = self.client.get('/user/home/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    # Check if correct data is displayed for the student
    self.assertContains(response, 'Test Status')
    self.assertContains(response, 'Test Course')

    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Load the homepage
    response = self.client.get('/user/home/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    # Check if the correct data is displayed for the teacher
    self.assertContains(response, 'Test Status')
    self.assertContains(response, 'Test Course')
    self.assertContains(response, 'Search')

  # User Test 2: Teachers can search for other users
  def test_search_users_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Search for a student
    response = self.client.get('/user/search/?query=student_1')
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    # Check if the page contains the student's username homepage information
    response = self.client.get('/user/search/1/')
    self.assertContains(response, self.student_user.username)

  # User Test 3: Teachers can view other user profiles
  def test_show_profile_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # View a student's profile
    response = self.client.get('/user/search/1/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.student_user.username)
    self.assertContains(response, self.course.course_title)

  # User Test 4: Users can read all notifications
  def test_all_notifications_function(self):
    # Create notifications for the student
    Notification.objects.create(user=self.student_app_user, message='New course material uploaded for Test Course by teacher_1')
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # View all notifications
    response = self.client.get('/user/notification/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    # Check if the page contains the necessary notifications
    self.assertContains(response, 'New course material uploaded for Test Course by teacher_1')

  # User Test 5: Teachers and students both can view their own profile information
  def test_user_profile_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # View the student's profile
    response = self.client.get('/user/profile/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.student_user.username)
    self.assertContains(response, self.student_app_user.real_name)
    self.assertContains(response, self.student_app_user.bio)

    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # View the teacher's profile
    response = self.client.get('/user/profile/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.teacher_user.username)
    self.assertContains(response, self.teacher_app_user.real_name)
    self.assertContains(response, self.teacher_app_user.bio)

  # User Test 6: Teachers can view other users profile information
  def test_show_information_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # View a student's information
    response = self.client.get('/user/search/1/info/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, self.student_user.username)
    self.assertContains(response, self.student_user.email)
    self.assertContains(response, self.student_app_user.real_name)
    self.assertContains(response, self.student_app_user.bio)

  # User Test 7: Users can edit their profile information
  def test_edit_profile_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # Edit the student's profile
    response = self.client.post('/user/profile/edit/', {'real_name': 'Updated Student One', 'bio': 'Updated Bio'})
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/profile/')
    self.student_app_user.refresh_from_db()
    # Check if the profile was edited
    self.assertEqual(self.student_app_user.real_name, 'Updated Student One')
    self.assertEqual(self.student_app_user.bio, 'Updated Bio')