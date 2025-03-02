from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.models import AppUser
from .models import Course, Notification
from .forms import CourseForm, CourseFeedbackForm, CourseMaterialForm
from .tasks import process_course_materials

@login_required
def create_course(request):
  user_role = AppUser.objects.get(user=request.user)
  # Send an error message if the user is not a teacher
  if not user_role.is_teacher:
    messages.error(request, 'Only teachers can create courses.')
    return HttpResponseRedirect('/user/home/')
  
  if request.method == 'POST':
    form = CourseForm(request.POST)
    # Create a new course if the form is valid
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
  # Check if the course exists
  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  # Get the course
  course = courses.first()

  # Check if the user exists
  app_user = AppUser.objects.filter(user=request.user)
  if not app_user.exists():
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  # Get the user
  app_user = app_user.first()

  # Allow only students to enroll in courses
  if not app_user.is_student:
    messages.error(request, 'Only students can enroll in courses.')
    return HttpResponseRedirect('/user/home/')
  # Check if the user is already enrolled in the course
  if app_user in course.enrolled_students.all():
    messages.warning(request, 'You are already enrolled in this course.')
  else:
    # Enroll the student in the course
    course.enrolled_students.add(app_user)
    messages.success(request, 'You have successfully enrolled in the course.')
    # Notify the teacher of the enrollment
    Notification.objects.create(user=course.created_by, message=f'{app_user.user.username} has enrolled in your course {course.course_title}')
  
  return HttpResponseRedirect('/user/home/')

@login_required
def unenroll_course(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  # Get the course
  course = courses.first()

  app_user = AppUser.objects.filter(user=request.user)
  if not app_user.exists():
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  # Get the user
  app_user = app_user.first()

  # Warn the user if they are not enrolled in the course they are trying to unenroll from
  if app_user not in course.enrolled_students.all():
    messages.warning(request, 'You are not enrolled in this course.')
  else:
    # Unenroll the student from the course
    course.enrolled_students.remove(app_user)
    messages.success(request, 'You have successfully unenrolled from the course.')

  return HttpResponseRedirect('/user/home/')

@login_required
def delete_course(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  # Get the course
  course = courses.first()

  # Only the teacher who created the course can delete it
  if course.created_by.user != request.user:
    messages.error(request, 'You do not have permission to delete this course.')
    return HttpResponseRedirect('/user/home/')
  
  # Delete the course
  course.delete()
  messages.success(request, 'Course deleted successfully.')
  return HttpResponseRedirect('/user/home/')

@login_required
def load_feedbacks(request, course_id):
  courses = Course.objects.filter(id=course_id)

  if not courses.exists():
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')

  # Get the course then load the feedbacks for the course
  course = courses.first()
  feedbacks = course.course_feedbacks.all().order_by('-time_submitted')

  app_user = AppUser.objects.filter(user=request.user).first()
  
  if app_user is None:
    messages.error(request, 'User does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  # Allow only students to submit feedback
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

  # Only enrolled students can submit feedback for the course
  if app_user not in course.enrolled_students.all():
    messages.error(request, 'You are not enrolled in this course.')
    return HttpResponseRedirect('/user/home/')
  
  if request.method == 'POST':
    # Submit the feedback if the form is valid
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

  # Check if the user is enrolled in the course or is the creator of the course
  enrolled = app_user in course.enrolled_students.all()
  creator = app_user == course.created_by
  # Retrieve the enrolled students and course materials for the course
  enrolled_students = course.enrolled_students.all()
  course_materials = course.course_materials.all().order_by('-upload_time')

  return render(request, 'courses/course_page.html', { 'course': course, 'enrolled': enrolled, 'creator': creator, 'enrolled_students': enrolled_students, 'course_materials': course_materials })

@login_required
def remove_student(request, course_id, user_id):
  # Get the course and student
  course = Course.objects.filter(id=course_id).first()
  student = AppUser.objects.filter(id=user_id).first()

  if not course:
    messages.error(request, 'Course does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  if not student:
    messages.error(request, 'Student does not exist.')
    return HttpResponseRedirect('/user/home/')
  
  # Only the teacher who created the course can remove students
  if request.user != course.created_by.user:
    messages.error(request, 'You do not have permission to remove students.')
    return HttpResponseRedirect(f'/user/course/{course.id}/view/')
  
  # Remove the student from the course
  course.enrolled_students.remove(student)
  messages.success(request, 'Student removed successfully.')

  return HttpResponseRedirect(f'/user/course/{course.id}/view/')

@login_required
def upload_course_materials(request, course_id):
  course = Course.objects.get(id=course_id)
  app_user = AppUser.objects.get(user=request.user)

  # Only the teacher who created the course can upload course materials
  if app_user != course.created_by:
    messages.error(request, 'You do not have permission to upload course materials.')
    return HttpResponseRedirect(f'/user/course/{course.id}/view/')
  
  if request.method == "POST":
    # Upload the course materials if the form is valid
    form = CourseMaterialForm(request.POST, request.FILES)
    if form.is_valid():
      course_material = form.save(commit=False)
      course_material.course = course
      course_material.uploaded_by = app_user
      course_material.original_name = request.FILES['file'].name
      course_material.save()

      # Notify the enrolled students when new course materials are uploaded
      enrolled_students = course.enrolled_students.all()
      for student in enrolled_students:
        Notification.objects.create(user=student, message=f'New course material uploaded for {course.course_title} by {app_user.user.username}')

      # Process the course materials asynchronously
      process_course_materials.delay(course_id, app_user.id, course_material.title, course_material.file.path)
      messages.success(request, 'Course material uploaded successfully.')
      return HttpResponseRedirect(f'/user/course/{course.id}/view/')
    
  return HttpResponseRedirect(f'/user/course/{course.id}/view/')
