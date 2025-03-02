from django.test import TestCase
from django.contrib.auth.models import User
from users.models import AppUser
from courses.models import Course, CourseFeedback, Notification
from django.core.files.uploadedfile import SimpleUploadedFile

class TestCourses(TestCase):
  def setUp(self):
    # Create a student user
    self.student_user = User.objects.create_user(username='student_1', password='abcd')
    self.student_app_user = AppUser.objects.create(user=self.student_user, is_student=True)
    # Create a teacher user
    self.teacher_user = User.objects.create_user(username='teacher_1', password='abcd')
    self.teacher_app_user = AppUser.objects.create(user=self.teacher_user, is_teacher=True)
    # Create a course and enroll the student
    self.course = Course.objects.create(course_title='Test Course', course_description='Test Course Description', created_by=self.teacher_app_user)
    self.course.enrolled_students.add(self.student_app_user)
    self.course_feedback = CourseFeedback.objects.create(course=self.course, student=self.student_app_user, feedback_content="Test Feedback")
    
  # Courses Test 1: Teachers can create courses
  def test_create_course_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Create a new course
    response = self.client.post('/user/course/create/', {'course_title': 'Teacher 1 Course', 'course_description': 'Teacher 1 Course Description'})
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/home/')
    # Check if the course was created
    self.assertEqual(Course.objects.count(), 2)

  # Courses Test 2: Students can enroll in courses
  def test_enroll_course_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # Enroll in a course
    response = self.client.get('/user/course/enroll/1/')
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/home/')
    # Check if the student was enrolled in the course
    self.assertEqual(self.course.enrolled_students.count(), 1)

  # Courses Test 3: Students can unenroll from courses
  def test_unenroll_course_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # Unenroll from a course
    response = self.client.get('/user/course/unenroll/1/')
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/home/')
    # Check if the student was unenrolled from the course
    self.assertEqual(self.course.enrolled_students.count(), 0)

  # Courses Test 4: Teachers can delete courses
  def test_delete_course_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Delete a course
    response = self.client.get('/user/course/delete/1/')
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/home/')
    # Check if the course was deleted
    self.assertEqual(Course.objects.count(), 0)

  # Courses Test 5: Users can view feedbacks for a course
  def test_load_feedbacks_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Load the feedbacks for a course
    response = self.client.get('/user/course/1/feedback/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    # Check if the page contains the feedback
    self.assertContains(response, 'Test Feedback')

  # Courses Test 6: Students can submit feedback for a course
  def test_submit_feedback_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # Submit a feedback for a course
    response = self.client.post('/user/course/1/feedback/submit/', {'feedback_content': 'Test Feedback 2'})
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/course/1/feedback/')
    # Check if the feedback was submitted
    self.assertEqual(CourseFeedback.objects.count(), 2)
    self.assertEqual(CourseFeedback.objects.last().feedback_content, 'Test Feedback 2')

  # Courses Test 7: Students can view a course
  def test_view_course_function(self):
    # Login as a student
    self.client.login(username='student_1', password='abcd')
    # View a course
    response = self.client.get('/user/course/1/view/')
    # Check if the page loads correctly
    self.assertEqual(response.status_code, 200)
    # Check if the page contains the course title
    self.assertContains(response, 'Test Course')

  # Courses Test 8: Teachers can remove students from a course
  def test_remove_student_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Remove a student from a course
    response = self.client.get('/user/course/1/remove/1/')
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/course/1/view/')
    # Check if the student was removed from the course
    self.assertEqual(self.course.enrolled_students.count(), 0)

  # Courses Test 9: Teachers can upload course materials
  def test_upload_course_materials_function(self):
    # Login as a teacher
    self.client.login(username='teacher_1', password='abcd')
    # Create a placeholder test file
    test_file = SimpleUploadedFile('test_file.pdf', b'test_file_content', content_type='application/pdf')
    # Upload the test file as a course material
    response = self.client.post('/user/course/1/upload/', {'title': 'Test Material', 'file': test_file})
    # Check if the page redirects correctly
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/course/1/view/')
    # Check if the course material was uploaded
    self.assertEqual(self.course.course_materials.count(), 1)
    self.assertEqual(self.course.course_materials.last().title, 'Test Material')
    