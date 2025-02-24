from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from courses import views as courses_views

urlpatterns = [
    path('create/', login_required(login_url='/user/login/')(courses_views.create_course), name='create_course'),
    path('enroll/<int:course_id>/', login_required(login_url='/user/login/')(courses_views.enroll_course), name='enroll_course'),
    path('unenroll/<int:course_id>/', login_required(login_url='/user/login/')(courses_views.unenroll_course), name='unenroll_course'),
    path('delete/<int:course_id>/', login_required(login_url='/user/login/')(courses_views.delete_course), name='delete_course')
]