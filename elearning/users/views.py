from django.shortcuts import render
from .forms import UserProfileUpdateForm, UserStatusUpdateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from courses.models import Course
from .models import AppUser, UserStatusUpdate
from courses.models import Notification
from .tasks import process_profile_photos
from api.permissions import is_teacher


@login_required
def homepage(request):
    try:
        app_user = AppUser.objects.get(user=request.user)
    except AppUser.DoesNotExist:
        messages.error(request, "User not found.")
        return render(request, "authentication/login.html", {})

    # Retrieve the user's status updates
    status_list = UserStatusUpdate.objects.filter(user=request.user).order_by(
        "-time_posted"
    )
    # Check if the user is the owner of the profile
    own_profile = request.user == app_user.user

    # Display the different courses section based on the user's role
    if app_user.is_teacher:
        teacher_courses = Course.objects.filter(created_by=app_user).order_by(
            "-time_created"
        )
        student_courses = None
        enrolled_courses = None
    else:
        teacher_courses = None
        student_courses = Course.objects.all().order_by("-time_created")
        enrolled_courses = app_user.enrolled_students.all()

    # Handle the user status update request
    if request.method == "POST":
        status_form = UserStatusUpdateForm(request.POST)
        if status_form.is_valid():
            status = status_form.save(commit=False)
            status.user = request.user
            status.save()
            messages.success(request, "Status updated.")
            return HttpResponseRedirect("/user/home/")

    else:
        # Create the status form
        status_form = UserStatusUpdateForm()

    # Renders the homepage based on the user's role
    if app_user.is_student:
        return render(
            request,
            "users/student_homepage.html",
            {
                "status_list": status_list,
                "status_form": status_form,
                "student_courses": student_courses,
                "enrolled_courses": enrolled_courses,
                "own_profile": own_profile,
            },
        )
    elif app_user.is_teacher:
        return render(
            request,
            "users/teacher_homepage.html",
            {
                "status_list": status_list,
                "status_form": status_form,
                "teacher_courses": teacher_courses,
                "own_profile": own_profile,
            },
        )
    else:
        messages.error(request, "Pleaes login to view this page.")
        return HttpResponseRedirect("/auth/login/")


@login_required
def search_users(request):
    app_user = AppUser.objects.get(user=request.user)

    if not app_user.is_teacher:
        messages.error(request, "Only teachers can search for users.")
        return HttpResponseRedirect("/user/home/")

    # Get the request query and strip it
    query = request.GET.get("query", "")
    query = query.strip()

    # Redirect to the user's profile if the user exists
    if query:
        target_user = AppUser.objects.filter(user__username=query).first()

        if target_user:
            return HttpResponseRedirect(f"/user/search/{target_user.id}/")

        messages.error(request, "User not found.")

    return HttpResponseRedirect("/user/home/")


@login_required
@user_passes_test(is_teacher, login_url="/user/home/")
def show_profile(request, user_id):
    try:
        app_user = AppUser.objects.get(id=user_id)
    except AppUser.DoesNotExist:
        messages.error(request, "User does not exist.")
        return HttpResponseRedirect("/user/search/")

    # Retrieve the user's status updates
    status_list = UserStatusUpdate.objects.filter(user=app_user.user).order_by(
        "-time_posted"
    )
    # Check if the user is the owner of the profile
    own_profile = request.user == app_user.user
    is_student = False

    # Display the different courses section based on the user's role
    if app_user.is_teacher:
        teacher_courses = Course.objects.filter(created_by=app_user).order_by(
            "-time_created"
        )
        is_student = False
        return render(
            request,
            "users/teacher_homepage.html",
            {
                "app_user": app_user,
                "status_list": status_list,
                "teacher_courses": teacher_courses,
                "own_profile": own_profile,
                "is_student": is_student,
            },
        )

    elif app_user.is_student:
        student_courses = Course.objects.all().order_by("-time_created")
        enrolled_courses = app_user.enrolled_students.all()
        is_student = True
        return render(
            request,
            "users/student_homepage.html",
            {
                "app_user": app_user,
                "status_list": status_list,
                "student_courses": student_courses,
                "enrolled_courses": enrolled_courses,
                "own_profile": own_profile,
                "is_student": is_student,
            },
        )

    messages.error(request, "Please log in to continue.")
    return HttpResponseRedirect("/auth/login/")


@login_required
def all_notifications(request):
    # Return all the notifications for the user
    app_user = AppUser.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=app_user).order_by("-time_created")
    # Set all the notifications to read
    notifications.update(read=True)

    return render(request, "users/notifications.html", {"notifications": notifications})


@login_required
def user_profile(request):
    # Retrieve the user's profile information of the logged in user
    app_user = AppUser.objects.get(user=request.user)
    own_profile = app_user.user == request.user

    return render(
        request,
        "users/user_profile.html",
        {"app_user": app_user, "own_profile": own_profile},
    )


@login_required
@user_passes_test(is_teacher, login_url="/user/home/")
def show_information(request, user_id):
    # Retrieve the user's profile information based on the user ID
    app_user = AppUser.objects.get(id=user_id)
    own_profile = app_user.user == request.user

    return render(
        request,
        "users/user_profile.html",
        {"app_user": app_user, "own_profile": own_profile},
    )


@login_required
def edit_profile(request):
    app_user = AppUser.objects.get(user=request.user)

    if request.method == "POST":
        profile_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=app_user
        )

        if profile_form.is_valid():
            # Save the updated profile information
            updated_profile = profile_form.save(commit=False)
            updated_profile.user = request.user
            updated_profile.save()

            # Process the profile photo asynchronously if it's submitted
            if "profile_photo" in request.FILES:
                process_profile_photos.delay(updated_profile.id)

            messages.success(request, "Profile updated.")
            return HttpResponseRedirect("/user/profile/")

        else:
            messages.error(request, "Error updating profile. Please check your input.")
            HttpResponseRedirect("/user/profile/edit/")

    else:
        # Create the profile form
        profile_form = UserProfileUpdateForm(instance=app_user)

    return render(
        request,
        "users/edit_profile.html",
        {"profile_form": profile_form, "app_user": app_user},
    )
