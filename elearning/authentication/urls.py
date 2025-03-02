from django.urls import path
from django.contrib.auth.decorators import login_required
from authentication import views as auth_views

urlpatterns = [
  path('register/', auth_views.user_register, name='register'),
  path('login/', auth_views.user_login, name='login'),
  path('logout/', login_required(login_url='/auth/login/')(auth_views.user_logout), name='logout'),
]