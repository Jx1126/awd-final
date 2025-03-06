from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def user_register(request):
    if request.method == "POST":
        # Get the data from the forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Save the user data and profile to the database
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                # Save the profile data
                profile = profile_form.save(commit=False)
                profile.user = user

                # Set the user role
                user_role = profile_form.cleaned_data["user_role"]
                if user_role == "student":
                    profile.is_student = True
                elif user_role == "teacher":
                    profile.is_teacher = True

                # Save the profile data to the database
                profile.save()
                messages.success(request, "You have successfully registered.")
                return HttpResponseRedirect("/auth/login/")

            except Exception as e:
                messages.error(request, f"Error: {e}")

        else:
            messages.error(request, "Username taken. Please choose another username.")

    else:
        # Create the forms
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "authentication/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def user_login(request):
    if request.method == "POST":
        # Get data from the form
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate the user
        user = authenticate(username=username, password=password)

        # Login the user if the user exists and is active
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return HttpResponseRedirect("/user/home/")
            else:
                messages.error(request, "This account is disabled.")
                return render(request, "authentication/login.html", {})
        else:
            messages.error(request, "Invalid login.")
            return render(request, "authentication/login.html", {})

    else:
        return render(request, "authentication/login.html", {})


@login_required
def user_logout(request):
    # Log the user out
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return HttpResponseRedirect("/auth/login/")
