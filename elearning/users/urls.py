from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('register/', user_views.user_register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', user_views.user_logout, name='logout'),
]