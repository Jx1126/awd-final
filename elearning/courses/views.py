from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.models import AppUser
from .models import Course
from .forms import CourseForm

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
