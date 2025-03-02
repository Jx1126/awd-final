from django.test import TestCase
from django.contrib.auth.models import User
from users.models import AppUser

class TestAuthentication(TestCase):
  # Setup data for the test case
  def setUp(self):
    self.user = User.objects.create_user(username='student_1', password='abcd')
    self.app_user = AppUser.objects.create(user=self.user, is_student=True, real_name='Johnny')

  # Authentication Test 1: Registration page loads
  def test_registration_loads(self):
    response = self.client.get('/auth/register/')
    self.assertEqual(response.status_code, 200)

  # Authentication Test 2: Login page loads
  def test_login_loads(self):
    response = self.client.get('/auth/login/')
    self.assertEqual(response.status_code, 200)

  # Authetication Test 3: User exists after registration
  def test_registration_function(self):
    response = self.client.post('/auth/register/', {
      'username': 'student_2',
      'email': 'student2@gmail.com',
      'password': 'abcd',
      'real_name': 'Bruno',
      'user_role': 'student',
      'bio': 'Hello I am Bruno',
    })
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/auth/login/')
    self.assertTrue(User.objects.filter(username='student_2').exists())

  # Authentication Test 4: User can login with the correct credentials
  def test_login_function(self):
    response = self.client.post('/auth/login/', {'username': 'student_1' ,'password': 'abcd',})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/user/home/')
    self.assertTrue(response.wsgi_request.user.is_authenticated)

  # Authentication Test 5: User can logout
  def test_logout_function(self):
    self.client.login(username='student_1', password='abcd')
    response = self.client.get('/auth/logout/')
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/auth/login/')
    self.assertFalse(response.wsgi_request.user.is_authenticated)