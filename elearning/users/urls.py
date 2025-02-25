from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from users import views as user_views

urlpatterns = [
    path('register/', user_views.user_register, name='register'),
    path('login/', user_views.user_login, name='login'),
    path('logout/', login_required(login_url='login/')(user_views.user_logout), name='logout'),
    path('home/', login_required(login_url='login/')(user_views.homepage), name='home'),
    path('search/', login_required(login_url='login/')(user_views.search_users), name='search_users'),
    path('search/<int:user_id>/', login_required(login_url='login/')(user_views.show_profile), name='show_profile'),
]