from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.models import AppUser
from .models import Course
from .forms import CourseForm, CourseFeedbackForm

@login_required
def create_course(request):
  user_role = AppUser.objects.get(user=request.user)
  if not user_role.is_teacher:
    messages.error(request, 'Only teachers can create courses.')
    return HttpResponseRedirect('/user/home/')
  
  if request.method == 'POST':
    form = CourseForm(request.POST)
    if form.is_valid():
      course = form.save(commit=False)
      course.created_by = AppUser.objects.get(user=request.user)
      course.save()
      messages.success(request, 'Course created successfully!')
      return HttpResponseRedirect('/user/home/')
  else:
    create_form = CourseForm()

  return render(request, 'courses/create_course.html', { 'create_form': create_form })

@login_required
def enroll_course(request, course_id):

  courses = Course.objects.filter(id=course_id)
  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  course = courses.first()

  app_user = AppUser.objects.filter(user=request.user)
  if not app_user.exists():
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  app_user = app_user.first()

  if not app_user.is_student:
    messages.error(request, 'Only students can enroll in courses.')
    return HttpResponseRedirect('/user/home/')
  
  if app_user in course.enrolled_students.all():
    messages.warning(request, 'You are already enrolled in this course.')
  else:
    course.enrolled_students.add(app_user)
    messages.success(request, 'You have successfully enrolled in the course.')
  
  return HttpResponseRedirect('/user/home/')

@login_required
def unenroll_course(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  course = courses.first()

  app_user = AppUser.objects.filter(user=request.user)
  if not app_user.exists():
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  app_user = app_user.first()

  if app_user not in course.enrolled_students.all():
    messages.warning(request, 'You are not enrolled in this course.')
  else:
    course.enrolled_students.remove(app_user)
    messages.success(request, 'You have successfully unenrolled from the course.')

  return HttpResponseRedirect('/user/home/')

@login_required
def delete_course(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  course = courses.first()

  if course.created_by.user != request.user:
    messages.error(request, 'You do not have permission to delete this course.')
    return HttpResponseRedirect('/user/home/')
  
  course.delete()
  messages.success(request, 'Course deleted successfully.')
  return HttpResponseRedirect('/user/home/')

@login_required
def load_feedbacks(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  course = courses.first()
  feedbacks = course.course_feedbacks.all().order_by('-time_submitted')

  app_user = AppUser.objects.filter(user=request.user).first()
  
  if app_user is None:
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  feedback_form = None
  if app_user.is_student and app_user in course.enrolled_students.all():
    feedback_form = CourseFeedbackForm()
    
  return render(request, 'courses/course_feedback.html', { 'course': course, 'feedbacks': feedbacks, 'feedback_form': feedback_form })

@login_required
def submit_feedback(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  course = courses.first()

  app_user = AppUser.objects.filter(user=request.user)
  if not app_user.exists():
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  app_user = app_user.first()

  if app_user not in course.enrolled_students.all():
    messages.error(request, 'You are not enrolled in this course.')
    return HttpResponseRedirect('/user/home/')
  
  if request.method == 'POST':
    feedback_form = CourseFeedbackForm(request.POST)
    if feedback_form.is_valid():
      feedback = feedback_form.save(commit=False)
      feedback.course = course
      feedback.student = app_user
      feedback.save()
      messages.success(request, 'Feedback submitted successfully.')
      return HttpResponseRedirect(f'/user/course/{course.id}/feedback/')
    
@login_required
def view_course(request, course_id):
  course = Course.objects.filter(id=course_id).first()
  
  if not course:
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  app_user = AppUser.objects.get(user=request.user)

  enrolled = app_user in course.enrolled_students.all()
  creator = app_user == course.created_by
  enrolled_students = course.enrolled_students.all()

  return render(request, 'courses/course_page.html', { 'course': course, 'enrolled': enrolled, 'creator': creator, 'enrolled_students': enrolled_students })

@login_required
def remove_student(request, course_id, user_id):
  course = Course.objects.filter(id=course_id).first()
  student = AppUser.objects.filter(id=user_id).first()

  if not course:
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  if not student:
    messages.error(request, 'Student does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  if request.user != course.created_by.user:
    messages.error(request, 'You do not have permission to remove students.')
    return HttpResponseRedirect(f'/user/course/{course.id}/view/')
  
  course.enrolled_students.remove(student)
  messages.success(request, 'Student removed successfully.')

  return HttpResponseRedirect(f'/user/course/{course.id}/view/')