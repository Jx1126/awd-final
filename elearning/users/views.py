from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
  status_list = UserStatusUpdate.objects.filter(user=request.user).order_by('-time_posted')

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
  try:
    app_user = AppUser.objects.get(user=request.user) 
  except AppUser.DoesNotExist:
    messages.error(request, 'User not found.')
    return render(request, 'users/login.html', {})

  if app_user.is_student:
    return render(request, 'users/student_homepage.html', {'status_list': status_list, 'status_form': status_form})
  elif app_user.is_teacher:
    return render(request, 'users/teacher_homepage.html', {'status_list': status_list, 'status_form': status_form})
  else:
    messages.error(request, 'Pleaes login to view this page.')
    return HttpResponseRedirect('/user/login/')