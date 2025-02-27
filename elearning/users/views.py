from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import AppUser
from courses.models import Notification
from .tasks import process_profile_photos

def user_register(request):

  if request.method == 'POST':
    # Get the data from the forms
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      try:
        # Save the user data and profile to the database
        user = user_form.save()
        user.set_password(user.password)
        user.save()

        profile = profile_form.save(commit=False)
        profile.user = user

        # Check if the user is a student or teacher
        user_role = profile_form.cleaned_data['user_role']
        if user_role == 'student':
          profile.is_student = True
        elif user_role == 'teacher':
          profile.is_teacher = True

        # Save the profile data to the database
        profile.save()
        messages.success(request, 'You have successfully registered.')
        return HttpResponseRedirect('/user/login/')
      
      except Exception as e:
        messages.error(request, f'Error: {e}')
    
    else:
      messages.error(request, 'Username taken. Please choose another username.')

  else:
    # Create the forms
    user_form = UserForm()
    profile_form = UserProfileForm()

  return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user:
      if user.is_active:
        login(request, user)
        messages.success(request, 'You have successfully logged in.')
        return HttpResponseRedirect('/user/home/')
      else:
        messages.error(request, 'This account is disabled.')
        return render(request, 'users/login.html', {})
    else:
      messages.error(request, 'Invalid login.')
      return render(request, 'users/login.html', {})

  else:
    return render(request, 'users/login.html', {})

@login_required
def user_logout(request):
  logout(request)
  messages.success(request, 'You have successfully logged out.')
  return HttpResponseRedirect('/user/login/')

@login_required
def homepage(request):
  try:
    app_user = AppUser.objects.get(user=request.user) 
  except AppUser.DoesNotExist:
    messages.error(request, 'User not found.')
    return render(request, 'users/login.html', {})
  
  status_list = UserStatusUpdate.objects.filter(user=request.user).order_by('-time_posted')
  own_profile = (request.user == app_user.user)

  if app_user.is_teacher:
    teacher_courses = Course.objects.filter(created_by=app_user).order_by('-time_created')
    student_courses = None
    enrolled_courses = None
  else:
    teacher_courses = None
    student_courses = Course.objects.all().order_by('-time_created')
    enrolled_courses = app_user.enrolled_students.all()

  if request.method == 'POST':
    status_form = UserStatusUpdateForm(request.POST)
    if status_form.is_valid():
      status = status_form.save(commit=False)
      status.user = request.user
      status.save()
      messages.success(request, 'Status updated.')
      return HttpResponseRedirect('/user/home/')

  else:
    status_form = UserStatusUpdateForm()

  # Renders the homepage based on the user's role
  if app_user.is_student:
    return render(request, 'users/student_homepage.html', {'status_list': status_list, 'status_form': status_form, 'student_courses': student_courses, 'enrolled_courses': enrolled_courses, 'own_profile': own_profile})
  elif app_user.is_teacher:
    return render(request, 'users/teacher_homepage.html', {'status_list': status_list, 'status_form': status_form, 'teacher_courses': teacher_courses, 'own_profile': own_profile})
  else:
    messages.error(request, 'Pleaes login to view this page.')
    return HttpResponseRedirect('/user/login/')
  
@login_required
def search_users(request):
  app_user = AppUser.objects.get(user=request.user)

  if not app_user.is_teacher:
    messages.error(request, 'Only teachers can search for users.')
    return HttpResponseRedirect('/user/home/')
  
  query = request.GET.get('query', '')
  query = query.strip()

  if query:
    target_user = AppUser.objects.filter(user__username=query).first()

    if target_user:
      return HttpResponseRedirect(f'/user/search/{target_user.id}/')
    
    messages.error(request, 'User not found.')

  return HttpResponseRedirect('/user/home/')

@login_required
def show_profile(request, user_id):
  try:
    app_user = AppUser.objects.get(id=user_id)
  except AppUser.DoesNotExist:
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/search/')
  
  status_list = UserStatusUpdate.objects.filter(user=app_user.user).order_by('-time_posted')
  own_profile = (request.user == app_user.user)
  is_student = False

  if app_user.is_teacher:
    teacher_courses = Course.objects.filter(created_by=app_user).order_by('-time_created')
    is_student = False
    return render(request, 'users/teacher_homepage.html', {'app_user': app_user, 'status_list': status_list, 'teacher_courses': teacher_courses, 'own_profile': own_profile, 'is_student': is_student})
  
  elif app_user.is_student:
    student_courses = Course.objects.all().order_by('-time_created')
    enrolled_courses = app_user.enrolled_students.all()
    is_student = True
    return render(request, 'users/student_homepage.html', {'app_user': app_user, 'status_list': status_list, 'student_courses': student_courses, 'enrolled_courses': enrolled_courses, 'own_profile': own_profile, 'is_student': is_student})
  
  messages.error(request, 'Please log in to continue.')
  return HttpResponseRedirect('/user/login/')

@login_required
def all_notifications(request):
  app_user = AppUser.objects.get(user=request.user)
  notifications = Notification.objects.filter(user=app_user).order_by('-time_created')
  notifications.update(read=True)

  return render(request, 'users/notifications.html', {'notifications': notifications})

@login_required
def user_profile(request):
  app_user = AppUser.objects.get(user=request.user)
  own_profile = app_user.user == request.user

  return render(request, 'users/user_profile.html', {'app_user': app_user, 'own_profile': own_profile})

@login_required
def edit_profile(request):
  app_user = AppUser.objects.get(user=request.user)

  if request.method == 'POST':
    profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=app_user)

    if profile_form.is_valid(): 
      updated_profile = profile_form.save(commit=False)
      updated_profile.user = request.user
      updated_profile.save()

      if 'profile_photo' in request.FILES:
        process_profile_photos.delay(updated_profile.id)

      messages.success(request, 'Profile updated.')
      return HttpResponseRedirect('/user/profile/')
    
    else:
      messages.error(request, 'Error updating profile. Please check your input.')
      HttpResponseRedirect('/user/profile/edit/')

  else:
    profile_form = UserProfileUpdateForm(instance=app_user)
  
  return render(request, 'users/edit_profile.html', {'profile_form': profile_form, 'app_user': app_user})