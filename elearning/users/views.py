from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def user_register(request):
  registered = False

  if request.method == 'POST':
    # Get the data from the forms
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid and profile_form.is_valid():
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
        profile.is_teacher = False
      elif user_role == 'teacher':
        profile.is_teacher = True
        profile.is_student = False

      # Save the user profile data if it exists
      if 'real_name' in request.POST:
        profile.real_name = request.POST['real_name']

      if 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']

      if 'bio' in request.POST:
        profile.bio = request.POST['bio']

      # Save the profile data to the database
      profile.save()
      registered = True

  else:
    # Create the forms
    user_form = UserForm()
    profile_form = UserProfileForm()

  return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/user/home/')
      else:
        return render(request, 'error.html', {'error_message': 'This account is disabled.'})
    else:
      return render(request, 'error.html', {'error_message': 'Invalid login.'})

  else:
    return render(request, 'users/login.html', {})

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/user/login/')

@login_required
def homepage(request):
  status_list = UserStatusUpdate.objects.filter(user=request.user).order_by('-time_posted')

  if request.method == 'POST':
    status_form = UserStatusUpdateForm(request.POST)
    if status_form.is_valid():
      status = status_form.save(commit=False)
      status.user = request.user
      status.save()
      return HttpResponseRedirect('/user/home/')

  else:
    status_form = UserStatusUpdateForm()

  # Renders the homepage based on the user's role
  try:
    app_user = AppUser.objects.get(user=request.user) 
  except AppUser.DoesNotExist:
    return render(request, 'error.html', {'error_message': 'User not found.'})

  if app_user.is_student:
    return render(request, 'users/student_homepage.html', {'status_list': status_list, 'status_form': status_form})
  elif app_user.is_teacher:
    return render(request, 'users/teacher_homepage.html', {'status_list': status_list, 'status_form': status_form})
  else:
    return render(request, 'error.html', {'error_message': 'Please log in to view this page.'})