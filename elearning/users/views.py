from django.shortcuts import render
from .forms import *

def register(request):
  registered = False

  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    if user_form.is_valid and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      profile = profile_form.save(commit=False)
      profile.user = user

      user_role = profile_form.cleaned_data['user_role']
      if user_role == 'student':
        profile.is_student = True
        profile.is_teacher = False
      elif user_role == 'teacher':
        profile.is_teacher = True
        profile.is_student = False

      if 'real_name' in request.POST:
        profile.real_name = request.POST['real_name']

      if 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']

      if 'bio' in request.POST:
        profile.bio = request.POST['bio']

      profile.save()
      registered = True

  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})