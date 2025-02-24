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