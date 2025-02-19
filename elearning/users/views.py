from django.shortcuts import render
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

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
        return HttpResponseRedirect('/')
      else:
        return render(request, 'error.html', {'error_message': 'This account is disabled.'})
    else:
      return render(request, 'error.html', {'error_message': 'Invalid login.'})

  else:
    return render(request, 'users/login.html', {})
  
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')