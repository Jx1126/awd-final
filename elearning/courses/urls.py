from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from courses import views as courses_views

urlpatterns = [
    path('create/', login_required(login_url='user/login/')(courses_views.create_course), name='create_course'),
]